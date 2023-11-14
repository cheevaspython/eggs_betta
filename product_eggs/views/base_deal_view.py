from collections import OrderedDict

from dataclasses import asdict

from datetime import datetime

from rest_framework import status, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product_eggs.models.comment import CommentEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.permissions.apps_permission import USER_ROLES_SUPER
from product_eggs.permissions.calc_permissions import (
    check_create_calculate_user_permission,
    check_create_conf_calculate_user_permission,
    check_edit_calculate_permission, check_edit_conf_calculate_permission
)
from product_eggs.permissions.deal_permissions import (
    check_create_deal_permission, check_edit_deal_permission
)
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.serializers.additional_expense_serializers import AdditionalExpenseSerializer
from product_eggs.serializers.base_deal_serializers import (
    BaseDealEggsSerializer, CalculateEggsSerializer,
    ConfirmedCalculateEggsSerializer
)
from product_eggs.serializers.comments_serializers import CommentEggSerializer
from product_eggs.services.balance import add_balance_to_client_if_havent
from product_eggs.services.base_deal.conf_calc_service import (
    check_calc_ready_for_true, check_fields_values_to_calc_ready,
    check_validated_data_for_logic_conf, expence_create_new_model
)
from product_eggs.services.base_deal.db_orm import get_base_deal_orm_request
from product_eggs.services.base_deal.deal_status_change import DealStatusChanger
from product_eggs.services.base_deal.deal_services import (
    base_deal_edit_saver, base_deal_logs_saver, check_pre_status_for_create,
    check_relation_return_new_deal_docs,
    delivery_by_seller_check_and_return_logic, status_check
)
from product_eggs.services.comments import parse_comment_tmp_json
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from product_eggs.services.validation.check_validated_data import check_data_for_note
from product_eggs.services.dates_check import validate_datas_for_positive
from product_eggs.services.logic_hide_fields import  (
    get_return_edited_hide_data, init_logic_user
)
from product_eggs.services.validation.validate_fields import check_for_date_and_validate_them
from product_eggs.services.validation.validation_of_mass_egg import ValidationMassEggs
from users.models import CustomUser


class BaseDealModelViewSet(viewsets.ViewSet):
    """
    Base deal handler,
    calc, conf_calc, deal, completed deal.
    """
    queryset = BaseDealEggsModel.objects.all()

    @action(detail=True, methods=['post'])
    def create_calculate(self, request, pk=None) -> Response:
        check_create_calculate_user_permission(
            request.data,
            eq_requestuser_is_customuser(self.request.user)
        )
        serializer = BaseDealEggsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            entry_mass = ValidationMassEggs(serializer.validated_data)
            entry_mass.start_validate_mass()
            if isinstance(self.request.user, CustomUser):
                if self.request.user.role in USER_ROLES_SUPER:
                    pass
                else:
                    check_for_date_and_validate_them(serializer.validated_data)

            additional_expense_serializer = AdditionalExpenseSerializer(data=request.data)
            additional_expense_serializer.is_valid(raise_exception=True)

            if isinstance(additional_expense_serializer.validated_data, OrderedDict):
                serializer.validated_data['additional_expense'] = expence_create_new_model(additional_expense_serializer.validated_data)
            else:
                serializer.validated_data['additional_expense'] = expence_create_new_model()

            serializer.validated_data['owner'] = self.request.user
            serializer.validated_data['current_logic'] = None
            serializer.validated_data['documents'] = None

        #add comment model
            new_comment_model = CommentEggs.objects.create()
            new_comment_model.save()
            serializer.validated_data['comment_json'] = new_comment_model
            serializer.save()
        else:
            raise serializers.ValidationError('wrong data in create calc serializer error')

        instance = self.queryset.get(pk=serializer.data['id'])
        message = MessageLibrarrySend('confirm_new_calc', instance)
        message.send_message()
        base_deal_logs_saver(instance, serializer.data)
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def list_calculate(self, request, pk=None) -> Response:
        if serializer := get_base_deal_orm_request(1):
            if init_logic_user(request.user):
                return Response(get_return_edited_hide_data(serializer.data),
                    status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def patch_calculate(self, request, pk=None) -> Response:
        instance = BaseDealEggsModel.objects.get(pk=pk)
        check_edit_calculate_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        status_check(instance, [1])
        serializer = CalculateEggsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, dict):
            entry_mass = ValidationMassEggs(serializer.validated_data)
            entry_mass.start_validate_mass()

        if isinstance(serializer.validated_data, OrderedDict):
            if isinstance(self.request.user, CustomUser):
                if self.request.user.role in USER_ROLES_SUPER:
                    pass
                else:
                    validate_datas_for_positive(serializer.validated_data)

            if check_data_for_note(serializer.validated_data, instance, 'note_calc', request.user):
                serializer.validated_data['calc_to_confirm'] = False

            try:
                if serializer.validated_data['calc_to_confirm']:
                    message = MessageLibrarrySend('confirm_new_calc', instance)
                    message.send_message()
            except KeyError:
                pass
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def create_confirmed_calculate(self, request, pk=None) -> Response:
        check_create_conf_calculate_user_permission(
            eq_requestuser_is_customuser(self.request.user))
        instance = BaseDealEggsModel.objects.get(pk=pk)
        check_pre_status_for_create(instance, 1)
        serializer = ConfirmedCalculateEggsSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            # serializer.validated_data['additional_expense'] = check_field_expence_create_new_model(instance)
            serializer.validated_data['documents'] = check_relation_return_new_deal_docs(instance)
            if instance.delivery_by_seller:
                cur_logic = delivery_by_seller_check_and_return_logic(instance)
                serializer.validated_data['current_logic'] = cur_logic
                serializer.validated_data['logic_confirmed'] = True
                message1 = MessageLibrarrySend('calc_confirmed', instance)
                message1.send_message()
                message = MessageLibrarrySend('logic_confirmed_delivery_by_seller', instance)
                message.send_message()
                serializer.is_valid(raise_exception=True)
                serializer.save()
                base_deal_logs_saver(instance, serializer.data)
                return Response(status=status.HTTP_200_OK)

        message1 = MessageLibrarrySend('calc_confirmed', instance)
        message1.send_message()
        message2 = MessageLibrarrySend('conf_calc_wait_logic', instance)
        message2.send_message()
        serializer.is_valid(raise_exception=True)
        serializer.save()
        base_deal_logs_saver(instance, serializer.data)
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def list_confirmed_calculate(self, request, pk=None) -> Response:
        if serializer := get_base_deal_orm_request(2):
            if init_logic_user(request.user):
                return Response(get_return_edited_hide_data(serializer.data),
                    status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def patch_confirmed_calculate(self, request, pk=None) -> Response:
        instance = BaseDealEggsModel.objects.get(pk=pk)
        check_edit_conf_calculate_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        status_check(instance, [2])
        check_calc_ready_for_true(instance, request)
        serializer = ConfirmedCalculateEggsSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            entry_mass = ValidationMassEggs(serializer.validated_data)
            entry_mass.start_validate_mass()
            if isinstance(self.request.user, CustomUser):
                if self.request.user.role in USER_ROLES_SUPER:
                    pass
                else:
                    validate_datas_for_positive(serializer.validated_data)
            check_data_for_note(serializer.validated_data, instance, 'note_conf_calc', request.user)
            check_validated_data_for_logic_conf(serializer.validated_data, instance)
        serializer.save()
        if instance.calc_ready:
            if check_fields_values_to_calc_ready(instance):
                message = MessageLibrarrySend('calc_ready', instance)
                message.send_message()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def create_deal(self, request, pk=None) -> Response:
        check_create_deal_permission(
            eq_requestuser_is_customuser(self.request.user))
        instance = BaseDealEggsModel.objects.get(pk=pk)
        if request.data['entity'] == None:
            raise serializers.ValidationError('Для создания сделки необходимо добавить платежное Юр. лицо')
        check_pre_status_for_create(instance, 2)
        serializer = BaseDealEggsSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        for client in (instance.seller, instance.buyer, instance.current_logic):
            add_balance_to_client_if_havent(instance.entity.inn, client)

        if instance.postponement_pay_for_us > 0:
            instance.deal_status = 5
            instance.save()
            message = MessageLibrarrySend(
                'if_post_payment_to_seller', instance)
            message.send_message()
        else:
            deal = DealStatusChanger(
                instance, eq_requestuser_is_customuser(self.request.user))
            deal.status_changer_main()

        base_deal_logs_saver(instance, serializer.data)
        message = MessageLibrarrySend('conf_calc_confirmed_deal_create', instance)
        message.send_message()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def list_deal(self, request, pk=None) -> Response:
        if serializer := get_base_deal_orm_request(3):
            if init_logic_user(request.user):
                return Response(get_return_edited_hide_data(serializer.data),
                    status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def patch_deal(self, request, pk=None) -> Response | None:
        instance = BaseDealEggsModel.objects.get(pk=pk)
        check_edit_deal_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        status_check(instance, [3])
        serializer = BaseDealEggsSerializer(
            instance, data=request.data, partial=True)

        #parse comment
        serializer_comment = CommentEggSerializer(
            data=request.data)
        serializer_comment.is_valid(raise_exception=True)

        try:
            if isinstance(serializer_comment.validated_data, OrderedDict):
                if serializer_comment.validated_data['tmp_json']:
                    if data_for_save := parse_comment_tmp_json(
                            serializer_comment.validated_data, request.user):
                        serializer_comment.save()
                        if not instance.comment_json:
                            instance.comment_json = CommentEggs.objects.create()
                            instance.save()  #TODO
                        instance.comment_json.comment_body_json.update(
                            {str(datetime.today()): asdict(data_for_save)}
                        )
                        instance.comment_json.tmp_json = {}
                        instance.comment_json.save()

                serializer.is_valid(raise_exception=True)
                if isinstance(serializer.validated_data, OrderedDict):
                    entry_mass = ValidationMassEggs(serializer.validated_data)
                    entry_mass.start_validate_mass()
                    if isinstance(self.request.user, CustomUser):
                        if self.request.user.role in USER_ROLES_SUPER:
                            pass
                        else:
                            validate_datas_for_positive(serializer.validated_data)
                serializer.save()
                base_deal_edit_saver(instance, serializer.data, request.user)
                return Response(status=status.HTTP_200_OK)
            else:
                serializers.ValidationError('Нельзя редактировать сделку без комментария!!')
        except KeyError as e:
            raise serializers.ValidationError('Нельзя редактировать сделку без комментария!', e)
#
    @action(detail=True, methods=['patch'])
    def patch_deal_no_comment(self, request, pk=None) -> Response | None:
        instance = BaseDealEggsModel.objects.get(pk=pk)
        check_edit_deal_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        status_check(instance, [3])
        serializer = BaseDealEggsSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            entry_mass = ValidationMassEggs(serializer.validated_data)
            entry_mass.start_validate_mass()
            if isinstance(self.request.user, CustomUser):
                if self.request.user.role in USER_ROLES_SUPER:
                    pass
                else:
                    validate_datas_for_positive(serializer.validated_data)
        serializer.save() #TODO double save (in status 1, after chage to status 2 -> gerbage ws)
        change = DealStatusChanger(
            instance,
            eq_requestuser_is_customuser(self.request.user)
        )
        change.status_changer_main()

        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_model(self, request, pk=None) -> Response:
        instance = BaseDealEggsModel.objects.get(pk=pk)
        serializer = get_base_deal_orm_request(instance.status)
        if serializer:
            if init_logic_user(request.user):
                return Response(get_return_edited_hide_data(serializer.data),
                    status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Wrong status base deal', status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def list_comp_deal(self, request, pk=None) -> Response:
        if serializer := get_base_deal_orm_request(4):
            if init_logic_user(request.user):
                return Response(get_return_edited_hide_data(serializer.data),
                    status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
