from django.db.models import Prefetch
from django.db.models import Q

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from product_eggs.serializers.balance_serializers import StatisticBuyerClientSerializer, \
    StatisticSellerClientSerializer, StatisticLogicClientSerializer
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.base_client_serializers import BuyerCardEggsSerializerBukh, \
    LogicCardEggsSerializerBukh, SellerCardEggsSerializerBukh
from product_eggs.services.get_anything.try_to_get_models import get_client_for_inn
from product_eggs.permissions.validate_user import validate_user_for_statistic_page_change, \
    validate_user_for_statistic_page_list, validate_user_for_statistic_page_list_logic


class BalanceEggsViewSet(viewsets.ViewSet):
    """
    General balance ViewSet.
    For Seller and Buyer.
    """
    queryset = BuyerCardEggs.objects.all() 
    serializer_class = StatisticBuyerClientSerializer

    @action(detail=True, methods=['get'])
    def list_buyer(self, request, pk=None) -> Response:  
        """
        Balance buyer model.
        """
        validate_user_for_statistic_page_list(request)
        serializer = StatisticBuyerClientSerializer(
            BuyerCardEggs.objects.filter(
                    ~Q(balance=0) | ~Q(balance_form_one=0) | ~Q(balance_form_two=0)
                ).select_related(
                    'requisites', 'documents_contract').prefetch_related(
                    Prefetch('basedealeggsmodel_set',
                queryset=BaseDealEggsModel.objects.filter(
                    Q(deal_status__gt=1, is_active=True, status=3)))).order_by('balance'), many=True
            )
        return Response(serializer.data, status=status.HTTP_200_OK)    

    @action(detail=True, methods=['get'])
    def list_seller(self, request, pk=None) -> Response:  
        """
        Balance seller model.
        """
        validate_user_for_statistic_page_list(request)
        serializer = StatisticSellerClientSerializer(
            SellerCardEggs.objects.filter(
                    ~Q(balance=0) | ~Q(balance_form_one=0) | ~Q(balance_form_two=0)
                ).select_related(
                    'requisites', 'documents_contract').prefetch_related(
                    Prefetch('basedealeggsmodel_set',
                queryset=BaseDealEggsModel.objects.filter(
                    Q(deal_status__gt=1, is_active=True, status=3)))).order_by('balance'), many=True
            )
        return Response(serializer.data, status=status.HTTP_200_OK)    

    @action(detail=True, methods=['get'])
    def list_logic(self, request, pk=None) -> Response:  
        """
        Balance logic model.
        """
        validate_user_for_statistic_page_list_logic(request)
        serializer = StatisticLogicClientSerializer(
            LogicCardEggs.objects.filter(
                    ~Q(balance=0) | ~Q(balance_form_one=0) | ~Q(balance_form_two=0)
                ).select_related(
                    'requisites', 'documents_contract').prefetch_related(
                    Prefetch('basedealeggsmodel_set',
                queryset=BaseDealEggsModel.objects.filter(
                    Q(deal_status__gt=1, is_active=True, status=3)))).order_by('balance'), many=True
            )
        return Response(serializer.data, status=status.HTTP_200_OK)    

    @action(detail=True, methods=['get'])
    def list_clients_for_bukh(self, request, pk=None) -> Response:  
        """
        """
        # validate_user_for_statistic_page_list_logic(request)
        sellers = SellerCardEggsSerializerBukh(SellerCardEggs.objects.all().only('name', 'inn'), many=True)
        buyers = BuyerCardEggsSerializerBukh(BuyerCardEggs.objects.all().only('name', 'inn'), many=True)
        logics = LogicCardEggsSerializerBukh(LogicCardEggs.objects.all().only('name', 'inn'), many=True)

        return Response(
            {'sellers': sellers.data,
             'buyers': buyers.data,
             'logics': logics.data},
            status=status.HTTP_200_OK)    

    @action(detail=True, methods=['get'])
    def get_client(self, request, pk=None) -> Response: 
        validate_user_for_statistic_page_change(request)
        client_name_and_ser = {
            'SellerCardEggs': (SellerCardEggs, StatisticSellerClientSerializer),
            'BuyerCardEggs': (BuyerCardEggs, StatisticBuyerClientSerializer),
            'LogicCardEggs': (LogicCardEggs, StatisticLogicClientSerializer),
        }
        if pk:
            serializer = None
            serializer = client_name_and_ser[get_client_for_inn(pk).__class__.__name__][1](
                client_name_and_ser[get_client_for_inn(pk).__class__.__name__][0].objects.get(inn=pk)
            )
            if serializer:
                return Response(serializer.data, status=status.HTTP_200_OK)    

        return Response("Check entry data, pk is not found", status=status.HTTP_404_NOT_FOUND)    

