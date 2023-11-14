from django.db.models import Prefetch, Q, F

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.models.custom_model_viewset import CustomModelViewSet
from product_eggs.models.entity import EntityEggs
from product_eggs.serializers.balance_serializers import (
    BalanceBaseClientEggsSerializer, StatisticBuyerClientSerializer,
    StatisticSellerClientSerializer, StatisticLogicClientSerializer
)
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.base_client_serializers import (
    BuyerCardEggsSerializerBukh, LogicCardEggsSerializerBukh,
    SellerCardEggsSerializerBukh
)
from product_eggs.permissions.validate_user import (
    validate_user_for_statistic_page_list,
    validate_user_for_statistic_page_list_logic
)


class BalanceEggsModelViewSet(CustomModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = BalanceBaseClientEggs.objects.all()
    serializer_class = BalanceBaseClientEggsSerializer
    http_method_names = ['get', 'post', 'patch']


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
        return_book = dict()#[str, ReturnList]
        entitys = EntityEggs.objects.all()
        validate_user_for_statistic_page_list(request)
        for cur_entity in entitys:
            serializer = StatisticBuyerClientSerializer(
                BuyerCardEggs.objects.filter(
                        ~Q(cur_balance=None) & ~Q(cur_balance__balance=0) & Q(cur_balance__entity__inn=cur_entity.inn)
                ).select_related(
                    'requisites', 'manager', 'guest', 'documents_contract'
                ).prefetch_related(
                    'entitys'
                ).prefetch_related(
                    Prefetch(
                        'basedealeggsmodel_set', queryset=BaseDealEggsModel.objects.filter(
                            Q(deal_status__gte=3, is_active=True, status__gt=1, entity__inn=cur_entity.inn)))
                ).order_by('cur_balance__balance'), many=True)
            if serializer.data:
                return_book.update({cur_entity.inn: serializer.data})
        return Response(return_book, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def list_seller(self, request, pk=None) -> Response:
        """
        Balance seller model.
        """
        return_book = dict()#[str, ReturnList]
        entitys = EntityEggs.objects.all()
        validate_user_for_statistic_page_list(request)
        for cur_entity in entitys:
            serializer = StatisticSellerClientSerializer(
                SellerCardEggs.objects.filter(
                        ~Q(cur_balance=None) & ~Q(cur_balance__balance=0) & Q(cur_balance__entity__inn=cur_entity.inn)
                ).select_related(
                    'requisites', 'manager', 'guest', 'documents_contract'
                ).prefetch_related(
                    'entitys'
                ).prefetch_related(
                    Prefetch(
                        'basedealeggsmodel_set', queryset=BaseDealEggsModel.objects.filter(
                            Q(deal_status__gte=3, is_active=True, status__gt=2, entity__inn=cur_entity.inn)))
                ).order_by('cur_balance__balance'), many=True)
            if serializer.data:
                return_book.update({cur_entity.inn: serializer.data})
        return Response(return_book, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def list_logic(self, request, pk=None) -> Response:
        """
        Balance logic model.
        """
        return_book = dict()#[str, ReturnList]
        entitys = EntityEggs.objects.all()
        for cur_entity in entitys:
            validate_user_for_statistic_page_list_logic(request)
            serializer = StatisticLogicClientSerializer(
                    LogicCardEggs.objects.filter(
                        ~Q(cur_balance=None) & ~Q(cur_balance__balance=0) & Q(cur_balance__entity__inn=cur_entity.inn)
                ).select_related(
                    'requisites', 'manager', 'guest', 'documents_contract'
                ).prefetch_related(
                    'entitys'
                # ).prefetch_related(
                #     Prefetch('cur_balance', queryset=BalanceBaseClientEggs.objects.filter(
                #         entity__inn=cur_entity.inn
                #     )
                ).prefetch_related(
                    Prefetch(
                        'basedealeggsmodel_set', queryset=BaseDealEggsModel.objects.filter(
                            Q(deal_status__gte=3, is_active=True, status__gt=2, entity__inn=cur_entity.inn)))
                    ).order_by('cur_balance__balance'), many=True)
            if serializer.data: # and isinstance(serializer.data, ReturnList):
                return_book.update({cur_entity.inn: serializer.data})
        return Response(return_book, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def list_clients_for_bukh(self, request, pk=None) -> Response:
        """
        """
        # validate_user_for_statistic_page_list_logic(request)
        sellers = SellerCardEggsSerializerBukh(SellerCardEggs.objects.all().select_related(
            'requisites').prefetch_related('entitys').annotate(name=F('requisites__name')), many=True)
        logics = LogicCardEggsSerializerBukh(LogicCardEggs.objects.all().select_related(
            'requisites').prefetch_related('entitys').annotate(name=F('requisites__name')), many=True)
        buyers = BuyerCardEggsSerializerBukh(BuyerCardEggs.objects.all().select_related(
            'requisites').prefetch_related('entitys').annotate(name=F('requisites__name')), many=True)

        return Response({
                'sellers': sellers.data,
                 'buyers': buyers.data,
                 'logics': logics.data
            },
            status=status.HTTP_200_OK)











