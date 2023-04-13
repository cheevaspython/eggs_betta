from rest_framework import viewsets, permissions, response

from product_eggs.serializers.limit_buyers_eggs import StatisticClientSerializer
from product_eggs.serializers.base_card_serializers import BuyerCardEggsDetailSerializer, \
    SellerCardEggsDetailSerializer
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs
from product_eggs.services.base_client_services import get_client_for_inn
from product_eggs.permissions.validate_user import validate_user_for_statistic_page_change, \
    validate_user_for_statistic_page_list
from product_eggs.services.limit_duty_eggs import get_queryset_deals_debt_by_client_seller_if_true, \
    get_queryset_where_debt_positive, convert_ordereddict_data_to_list_of_dicts_and_add_field, \
    get_queryset_where_balance_seller_true
    

class LimitDutyEggsViewSet(viewsets.ViewSet):
    queryset = BuyerCardEggs.objects.all().select_related() 
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, format=None):  
        validate_user_for_statistic_page_list(request)
        serializer = StatisticClientSerializer(get_queryset_where_debt_positive(), many=True)
        edited_data = convert_ordereddict_data_to_list_of_dicts_and_add_field(serializer.data)
        return response.Response(edited_data) 

    def retrieve(self, request, pk, *args, **kwargs): 
        validate_user_for_statistic_page_change(request)
        instance = get_client_for_inn(pk)
        serializer, deals_debt_data = None, None
        if instance:
            if isinstance(instance, SellerCardEggs):
                serializer = SellerCardEggsDetailSerializer(instance)
                deals_debt_data = get_queryset_deals_debt_by_client_seller_if_true(pk, seller=True)
            elif isinstance(instance, BuyerCardEggs):
                serializer = BuyerCardEggsDetailSerializer(instance)
                deals_debt_data = get_queryset_deals_debt_by_client_seller_if_true(pk, seller=False)
        if serializer: 
            if deals_debt_data:
                return response.Response([serializer.data, deals_debt_data])
            else:
                return response.Response(serializer.data)
        return response.Response("chek entry data", 200)


class BalanceSellerEggs(viewsets.ViewSet):
    queryset = SellerCardEggs.objects.all().select_related('requisites', 'documents_contract') #TODO
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, format=None):  
        validate_user_for_statistic_page_list(request)
        serializer = SellerCardEggsDetailSerializer(get_queryset_where_balance_seller_true(), many=True)
        return response.Response(serializer.data)

    def patch(self, request):
        ...













