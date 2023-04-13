from rest_framework import response, permissions

from product_eggs.models.calcs_deal_eggs import DealEggs
from product_eggs.models.custom_model_viewset import CustomModelViewSet
from product_eggs.serializers.calc_deal_serializers_eggs import DealEggsDetailSerializer, DealEggsSerializer 
from product_eggs.permissions.deal_permissions import check_create_deal_permission, check_edit_deal_permission
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.services.deal_status import check_processing_to_confirm, send_message_if_post_payment_to_seller
from product_eggs.services.logic_hide_fields import init_logic_user, hide_fields_in_data, get_return_data
from product_eggs.services.message_send_save import search_done_calc_and_conf_calc_messages_and_turn_off_fields_is_value
from product_eggs.services.turn_off_fields import turn_off_fields_is_active
from product_eggs.services.add_select_related import deal_list_select_related_is_active
from product_eggs.services.deal_services import create_relation_deal_orig_and_docs_if_not_None
from product_eggs.services.calculate_margin import calculate_margin_python, add_margin_field_to_deal, \
    calculate_margin_python_import


class DealEggsViewSet(CustomModelViewSet):
    queryset = DealEggs.objects.all().select_related('confirmed_calculate', 'owner')   
    serializer_class = DealEggsSerializer
    permission_classes = [permissions.IsAuthenticated]    

    def perform_create(self, serializer):
        check_create_deal_permission(eq_requestuser_is_customuser(self.request.user))
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

        current_deal = self.queryset.get(id=serializer.data['id'])
        create_relation_deal_orig_and_docs_if_not_None(current_deal)

        if current_deal.pre_payment_application:
            check_processing_to_confirm(current_deal, eq_requestuser_is_customuser(self.request.user))
        else:
            current_deal.status = 5
            current_deal.save()
            send_message_if_post_payment_to_seller(current_deal)

        turn_off_fields_is_active(current_deal.confirmed_calculate)   #TODO
        search_done_calc_and_conf_calc_messages_and_turn_off_fields_is_value(current_deal.confirmed_calculate) #db n+1 check

    def perform_update(self, serializer, instance):
        check_edit_deal_permission(eq_requestuser_is_customuser(self.request.user), instance)
        serializer.save()
        check_processing_to_confirm(instance, eq_requestuser_is_customuser(self.request.user))

    def list(self, request, *args, **kwargs):
        deal_is_active = deal_list_select_related_is_active()
        add_margin_field_to_deal(deal_is_active)
        detail_serializer = DealEggsDetailSerializer(deal_is_active, many=True)

        if init_logic_user(request.user):
            return response.Response(get_return_data(detail_serializer.data))
                
        return response.Response(detail_serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.import_application:
            instance.margin = calculate_margin_python_import(instance, instance.delivery_cost,
                instance.confirmed_calculate.additional_expense.expense_total)
        else:
            instance.margin = calculate_margin_python(instance, instance.delivery_cost,
                instance.confirmed_calculate.additional_expense.expense_total)
        detail_serializer = DealEggsDetailSerializer(instance)

        if init_logic_user(request.user):
            return response.Response(hide_fields_in_data(detail_serializer.data))

        return response.Response(detail_serializer.data)


