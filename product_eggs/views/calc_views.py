from rest_framework import response, permissions

from product_eggs.serializers.calc_deal_serializers_eggs import CalculateEggsDetailSerializer, \
    ConfirmedCalculateEggsDetailSerializer, ConfirmedCalculateEggsSerializer, \
    CalculateEggsSerializer
from product_eggs.models.calcs_deal_eggs import CalculateEggs, ConfirmedCalculateEggs
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser, \
    verificate_user_as_superuser
from product_eggs.permissions.calc_permissions import check_create_calculate_user_permission, \
    check_create_conf_calculate_user_permission, check_edit_calculate_permission, \
    check_edit_conf_calculate_permission
from product_eggs.services.turn_off_fields import turn_off_fields_is_active
from product_eggs.services.validation_of_mass_egg import ValidationMassEggs
from product_eggs.services.dates_check import validation_delivery_interval, validate_calc_datas_for_positive
from product_eggs.services.check_validated_data import check_data_for_note
from product_eggs.services.logic_hide_fields import init_logic_user, hide_fields_in_data, \
    get_edit_conf_calculate_data, get_return_data, get_ediited_data
from product_eggs.services.calculate_margin import calculate_margin_python, add_margin_field_calculate, \
    add_margin_field_to_conf_calc, calculate_margin_python_import
from product_eggs.services.add_select_related import calc_list_select_related_is_active, \
    conf_calc_list_select_related_is_active
from product_eggs.services.confirmed_calc_services import create_related_conf_calc_and_additional_expense, \
    check_fields_calc_ready_send_message, check_calc_ready_for_true, \
    add_fields_to_conf_calc_if_delivery_by_seller, send_message_if_logic_confirmed
from product_eggs.services.messages_library import message_calculate_create, message_calc_confirmed, \
    message_conf_cal_to_logic
from product_eggs.models.custom_model_viewset import CustomModelViewSet


class CalculateEggsViewSet(CustomModelViewSet):
    queryset = CalculateEggs.objects.all().select_related(
        'application_from_buyer', 'application_from_seller', 'owner')
    serializer_class = CalculateEggsSerializer
    permission_classes = [permissions.IsAuthenticated]    

    def perform_create(self, serializer):
        check_create_calculate_user_permission(
            serializer.validated_data,
            eq_requestuser_is_customuser(self.request.user)
        )
        if verificate_user_as_superuser(eq_requestuser_is_customuser(self.request.user)):
            pass
        else:
            entry_mass = ValidationMassEggs(serializer.validated_data)
            entry_mass.start_validate_mass()
        validation_delivery_interval(serializer.validated_data['delivery_date_from_seller'], 
            serializer.validated_data['delivery_date_to_buyer'])
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

        current_calc = self.queryset.get(id=serializer.data['id'])
        message_calculate_create(current_calc)

    def perform_update(self, serializer, instance):
        check_edit_calculate_permission(eq_requestuser_is_customuser(self.request.user), instance)
        validate_calc_datas_for_positive(serializer.validated_data)   
        if verificate_user_as_superuser(eq_requestuser_is_customuser(self.request.user)):
            pass
        else:
            entry_mass = ValidationMassEggs(serializer.validated_data)
            entry_mass.start_validate_mass()
        serializer.save()
        check_data_for_note(serializer.data, instance) 

    def list(self, request, *args, **kwargs):
        calculate_is_active = calc_list_select_related_is_active()
        add_margin_field_calculate(calculate_is_active)
        detail_serializer = CalculateEggsDetailSerializer(calculate_is_active, many=True)

        if init_logic_user(request.user):
            return response.Response(get_return_data(detail_serializer.data))

        return response.Response(detail_serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.import_application:
            instance.margin = calculate_margin_python_import(instance, instance.delivery_cost)
        else:
            instance.margin = calculate_margin_python(instance, instance.delivery_cost)
        detail_serializer = CalculateEggsDetailSerializer(instance)

        if init_logic_user(request.user):
            return response.Response(hide_fields_in_data(detail_serializer.data))

        return response.Response(detail_serializer.data)


class ConfirmedCalculateEggsViewSet(CustomModelViewSet):
    queryset = ConfirmedCalculateEggs.objects.all().select_related(
        'current_calculate', 'current_logic', 'owner')
    serializer_class = ConfirmedCalculateEggsSerializer
    permission_classes = [permissions.IsAuthenticated]    

    def perform_create(self, serializer):
        check_create_conf_calculate_user_permission(eq_requestuser_is_customuser(self.request.user))
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

        current_conf_calc = self.queryset.get(id=serializer.data['id'])
        add_fields_to_conf_calc_if_delivery_by_seller(current_conf_calc)

        create_related_conf_calc_and_additional_expense(current_conf_calc)
        message_calc_confirmed(current_conf_calc)
        turn_off_fields_is_active((current_conf_calc.current_calculate, ))
        message_conf_cal_to_logic(current_conf_calc)

    def perform_update(self, serializer, instance):  
        check_edit_conf_calculate_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        if instance.is_active:
            check_calc_ready_for_true(instance)
        serializer.save()
        
        send_message_if_logic_confirmed(serializer.data, instance)
        check_data_for_note(serializer.data, instance) 
        if instance.calc_ready:   
            check_fields_calc_ready_send_message(instance)

    def list(self, request, *args, **kwargs):
        confirmed_calculate_is_active = conf_calc_list_select_related_is_active()
        add_margin_field_to_conf_calc(confirmed_calculate_is_active)
        detail_serializer = ConfirmedCalculateEggsDetailSerializer(confirmed_calculate_is_active, many=True)

        if init_logic_user(request.user):
                return response.Response(get_ediited_data(detail_serializer.data))

        return response.Response(detail_serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.current_calculate.import_application:
            instance.margin = calculate_margin_python_import(instance.current_calculate,
                instance.delivery_cost, instance.additional_expense.expense_total)
        else:
            instance.margin = calculate_margin_python(instance.current_calculate,
                instance.delivery_cost, instance.additional_expense.expense_total)
        detail_serializer = ConfirmedCalculateEggsDetailSerializer(instance)

        if init_logic_user(request.user):
                return response.Response(get_edit_conf_calculate_data(detail_serializer.data))

        return response.Response(detail_serializer.data)


