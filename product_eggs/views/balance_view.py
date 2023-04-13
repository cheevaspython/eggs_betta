from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from product_eggs.serializers.limit_duty_serializers import StatisticClientSerializer
from product_eggs.serializers.base_client_serializers import BuyerCardEggsDetailSerializer, \
    SellerCardEggsDetailSerializer
from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs
from product_eggs.services.get_anything.try_to_get_models import get_client_for_inn
from product_eggs.permissions.validate_user import validate_user_for_statistic_page_change, \
    validate_user_for_statistic_page_list
from product_eggs.services.balance_services import convert_serializer_data_to_list_of_dicts
from product_eggs.services.raw.balance import get_queryset_deals_debt_by_client, \
    get_queryset_deal_where_balance_seller_true, get_queryset_where_debt_positive 
    

class BalanceEggsViewSet(viewsets.ViewSet):
    """
    General balance ViewSet.
    For Seller and Buyer.
    """
    queryset = BuyerCardEggs.objects.all() 
    serializer_class = StatisticClientSerializer

    @action(detail=True, methods=['get'])
    def list_buyer(self, request, pk=None) -> Response:  
        """
        Balance buyer model.
        """
        validate_user_for_statistic_page_list(request)
        serializer = StatisticClientSerializer(
            get_queryset_where_debt_positive(), many=True)
        edited_data = convert_serializer_data_to_list_of_dicts(serializer.data)
        return Response(edited_data, status=status.HTTP_200_OK)    

    @action(detail=True, methods=['get'])
    def list_seller(self, request, pk=None) -> Response:  
        """
        Balance seller model.
        """
        validate_user_for_statistic_page_list(request)
        serializer = SellerCardEggsDetailSerializer(
            get_queryset_deal_where_balance_seller_true(), many=True)   
        return Response(serializer.data, status=status.HTTP_200_OK)    

    @action(detail=True, methods=['get'])
    def get_client(self, request, pk=None) -> Response: 
        validate_user_for_statistic_page_change(request)
        if pk:
            instance = get_client_for_inn(pk)
            serializer, deals_debt_data = None, None

            if isinstance(instance, SellerCardEggs):
                serializer = SellerCardEggsDetailSerializer(instance)
                deals_debt_data = get_queryset_deals_debt_by_client(pk, seller=True)
            elif isinstance(instance, BuyerCardEggs):
                serializer = BuyerCardEggsDetailSerializer(instance)
                deals_debt_data = get_queryset_deals_debt_by_client(pk, seller=False)

            if serializer: 
                if deals_debt_data:
                    return Response(
                        [serializer.data, deals_debt_data], status=status.HTTP_200_OK)    
                else:
                    return Response(serializer.data, status=status.HTTP_200_OK)    

        return Response("chek entry data", status=status.HTTP_200_OK)    

    # def get_seller(self, request) -> Response:
    #     ...


