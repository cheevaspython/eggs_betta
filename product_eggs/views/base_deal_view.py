from collections import OrderedDict

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product_eggs.models.base_client import LogicCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.permissions.calc_permissions import check_create_calculate_user_permission, \
    check_create_conf_calculate_user_permission, check_edit_calculate_permission, \
    check_edit_conf_calculate_permission
from product_eggs.permissions.deal_permissions import check_create_deal_permission, \
    check_edit_deal_permission
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.serializers.base_deal_serializers import BaseCompDealEggsNameSerializer, \
    BaseDealEggsNameSerializer, CalculateEggsNamesSerializer, CompleteDealEggsModelSerializer, \
    BaseDealEggsSerializer, CalculateEggsSerializer, ConfirmedCalculateEggsNameSerializer, \
    ConfirmedCalculateEggsSerializer
from product_eggs.services.base_deal.conf_calc_service import check_calc_ready_for_true, \
    check_field_expence_create_new_model, check_fields_values_to_calc_ready, \
    check_validated_data_for_logic_conf
from product_eggs.services.base_deal.deal_status_change import DealStatusChanger
from product_eggs.services.base_deal.deal_services import base_deal_logs_saver, \
    check_pre_status_for_create, create_relation_deal_status_and_deal_docs, status_check
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from product_eggs.services.validation.check_validated_data import check_data_for_note
from product_eggs.services.dates_check import validate_datas_for_positive
from product_eggs.services.logic_hide_fields import get_return_edited_hide_data, \
    init_logic_user
from product_eggs.services.validation.validate_fields import check_for_date_and_validate_them
from product_eggs.services.validation.validation_of_mass_egg import ValidationMassEggs


class BaseDealModelViewSet(viewsets.ViewSet):
    """
    Base deal handler, 
    calc, conf_calc, deal, completed deal.
    """
    queryset = BaseDealEggsModel.objects.all()
    serializer_class = CompleteDealEggsModelSerializer

    @action(detail=True, methods=['post'])
    def create_calculate(self, request, pk=None) -> Response:
        #TODO managers_id in pk
        check_create_calculate_user_permission(
            request.data,
            eq_requestuser_is_customuser(self.request.user)
        )
        # if verificate_user_as_superuser(eq_requestuser_is_customuser(self.request.user)):
        #     pass
        # else:
        serializer = BaseDealEggsSerializer(data=request.data) 
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            entry_mass = ValidationMassEggs(serializer.validated_data) 
            entry_mass.start_validate_mass()
            check_for_date_and_validate_them(serializer.validated_data)

            serializer.validated_data['owner'] = self.request.user
            serializer.validated_data['additional_expense'] = None
            serializer.validated_data['current_logic'] = None
            serializer.validated_data['documents'] = None
        serializer.save()

        instance = self.queryset.get(id=serializer.data['id'])
        message = MessageLibrarrySend('create_new_calc', instance)
        message.send_message()

        base_deal_logs_saver(instance, serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def list_calculate(self, request, pk=None) -> Response:
        serializer = CalculateEggsNamesSerializer(
            BaseDealEggsModel.objects.filter(
                is_active=True, status=1).select_related(
                    'seller', 'buyer', 'owner'), many=True
            )
        if init_logic_user(request.user):
            return Response(get_return_edited_hide_data(serializer.data),
                status=status.HTTP_200_OK)    
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def patch_calculate(self, request, pk=None) -> Response:
        # if verificate_user_as_superuser(eq_requestuser_is_customuser(self.request.user)):
        #     pass
        # else:
        instance = BaseDealEggsModel.objects.get(pk=pk)
        check_edit_calculate_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        status_check(instance, 1)
        serializer = CalculateEggsSerializer(instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            validate_datas_for_positive(serializer.validated_data)   
            check_data_for_note(serializer.validated_data, instance, 'note_calc') 
        if isinstance(serializer.validated_data, dict):
            entry_mass = ValidationMassEggs(serializer.validated_data) 
            entry_mass.start_validate_mass()
        serializer.save()

        #return list data for display
        serializer = CalculateEggsNamesSerializer(
            BaseDealEggsModel.objects.filter(
                is_active=True, status=1).select_related(
                    'seller', 'buyer', 'owner'), many=True
            )
        if init_logic_user(request.user):
            return Response(get_return_edited_hide_data(serializer.data),
                status=status.HTTP_200_OK)    
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def create_confirmed_calculate(self, request, pk=None) -> Response:   
        check_create_conf_calculate_user_permission(
            eq_requestuser_is_customuser(self.request.user))
        instance = BaseDealEggsModel.objects.get(pk=pk)
        create_relation_deal_status_and_deal_docs(instance)
        check_pre_status_for_create(instance, 1)
        serializer = ConfirmedCalculateEggsSerializer(
            instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            serializer.validated_data['additional_expense'] = \
                check_field_expence_create_new_model(instance)
            if instance.delivery_by_seller:
                serializer.validated_data['current_logic'] = LogicCardEggs.objects.get(id=1)
                message = MessageLibrarrySend('logic_confirmed', instance)
                message.send_message()
                 
        message1 = MessageLibrarrySend('calc_confirmed', instance)
        message1.send_message()
        message2 = MessageLibrarrySend('conf_calc_wait_logic', instance)
        message2.send_message()
        serializer.save()

        base_deal_logs_saver(instance, serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def list_confirmed_calculate(self, request, pk=None) -> Response:
        serializer = ConfirmedCalculateEggsNameSerializer(
            BaseDealEggsModel.objects.filter(
                is_active=True, status=2).select_related(
                    'seller', 'buyer', 'owner', 'additional_expense', 'current_logic'
                ), many=True
            )
        if init_logic_user(request.user):
            return Response(get_return_edited_hide_data(serializer.data),
                status=status.HTTP_200_OK)    
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def patch_confirmed_calculate(self, request, pk=None) -> Response:  
        instance = BaseDealEggsModel.objects.get(pk=pk)  
        check_edit_conf_calculate_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        status_check(instance, 2)
        check_calc_ready_for_true(instance)
        serializer = ConfirmedCalculateEggsSerializer(
            instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            entry_mass = ValidationMassEggs(serializer.validated_data) 
            entry_mass.start_validate_mass()
            validate_datas_for_positive(serializer.validated_data)   
            check_data_for_note(serializer.validated_data, instance, 'note_conf_calc') 
            check_validated_data_for_logic_conf(serializer.validated_data, instance)
        serializer.save()
        if instance.calc_ready:   
            if check_fields_values_to_calc_ready(instance):
                message = MessageLibrarrySend('calc_ready', instance)
                message.send_message()

        #return list data for display
        serializer = ConfirmedCalculateEggsNameSerializer(
            BaseDealEggsModel.objects.filter(
                is_active=True, status=2).select_related(
                    'seller', 'buyer', 'owner', 'additional_expense', 'current_logic'
                ),many=True
            )
        if init_logic_user(request.user):
            return Response(get_return_edited_hide_data(serializer.data),
                status=status.HTTP_200_OK)    
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def create_deal(self, request, pk=None) -> Response:  
        check_create_deal_permission(
            eq_requestuser_is_customuser(self.request.user))
        instance = BaseDealEggsModel.objects.get(pk=pk)  
        check_pre_status_for_create(instance, 2)
        #search_done_base_deal_messages_and_turn_off(instance) #TODO
        serializer = BaseDealEggsSerializer(
            instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)
        serializer.save()

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

        instance = base_deal_logs_saver(instance, serializer.data)
        instance.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def list_deal(self, request, pk=None) -> Response:  
        serializer = BaseDealEggsNameSerializer(
            BaseDealEggsModel.objects.filter(
                is_active=True, status=3).select_related(
                    'seller', 'buyer', 'owner', 'additional_expense', 'current_logic', 'documents'
                ), many=True
            )
        if init_logic_user(request.user):
            return Response(get_return_edited_hide_data(serializer.data),
                status=status.HTTP_200_OK)    

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def patch_deal(self, request, pk=None) -> Response:  
        instance = BaseDealEggsModel.objects.get(pk=pk)  
        check_edit_deal_permission(
            eq_requestuser_is_customuser(self.request.user), instance) 
        status_check(instance, 3)
        serializer = BaseDealEggsSerializer(
            instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            entry_mass = ValidationMassEggs(serializer.validated_data) 
            entry_mass.start_validate_mass()
            validate_datas_for_positive(serializer.validated_data)   
            # change = DealStatusChanger(instance,
            #     eq_requestuser_is_customuser(self.request.user))
        serializer.save()
        change = DealStatusChanger(instance,
            eq_requestuser_is_customuser(self.request.user))
        change.status_changer_main()

        #return list data for display
        serializer = BaseDealEggsNameSerializer(
            BaseDealEggsModel.objects.filter(
                is_active=True, status=3).select_related(
                    'seller', 'buyer', 'owner', 'additional_expense', 'current_logic', 'documents'
                ), many=True
            )
        if init_logic_user(request.user):
            return Response(get_return_edited_hide_data(serializer.data),
                status=status.HTTP_200_OK)    
        return Response(serializer.data, status=status.HTTP_200_OK)
#
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_model(self, request, pk=None) -> Response:
        instance = BaseDealEggsModel.objects.get(pk=pk)  
        match instance.status:
            case 1:
                serializer = CalculateEggsNamesSerializer(
                    BaseDealEggsModel.objects.filter(
                        is_active=True, status=1).select_related(
                            'seller', 'buyer', 'owner'), many=True
                    )
            case 2:
                serializer = ConfirmedCalculateEggsNameSerializer(
                    BaseDealEggsModel.objects.filter(
                        is_active=True, status=2).select_related(
                            'seller', 'buyer', 'owner', 'additional_expense', 'current_logic'
                        ), many=True
                    )
            case 3:
                serializer = BaseDealEggsNameSerializer(
                    BaseDealEggsModel.objects.filter(
                        is_active=True, status=3).select_related(
                            'seller', 'buyer', 'owner', 'additional_expense', 'current_logic', 'documents',
                        ), many=True
                    )
            case 4:
                serializer = BaseCompDealEggsNameSerializer(
                    BaseDealEggsModel.objects.filter(
                        is_active=True, status=4).select_related(
                            'seller', 'buyer', 'owner', 'additional_expense', 'current_logic', 'documents',
                        ), many=True
                    )
            case _:
                serializer = None
        if serializer:
            if init_logic_user(request.user):
                return Response(get_return_edited_hide_data(serializer.data),
                    status=status.HTTP_200_OK)    
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('Wrong status base deal', status=status.HTTP_200_OK)


    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def list_comp_deal(self, request, pk=None) -> Response:  
        serializer = BaseCompDealEggsNameSerializer(
            BaseDealEggsModel.objects.filter(
                is_active=True, status=4).select_related(
                    'seller', 'buyer', 'owner', 'additional_expense', 'current_logic', 'documents',
                ), many=True
            )
        if init_logic_user(request.user):
            return Response(get_return_edited_hide_data(serializer.data),
                status=status.HTTP_200_OK)    

        return Response(serializer.data, status=status.HTTP_200_OK)
