from typing import OrderedDict

from rest_framework import serializers, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.models.documents import DocumentsDealEggsModel, DocumentsContractEggsModel
from product_eggs.serializers.base_deal_serializers import BaseDealEggsFinanceDisciplineBuyerSerializer, BaseDealEggsFinanceDisciplineLogicSerializer, BaseDealEggsFinanceDisciplineSellerSerializer, BaseDealEggsGetPaymentsSerializer
from product_eggs.serializers.documents_serializers import (
    DocumentsDealEggsSerializer, DocumentsContractEggsSerializer,
    DocumentsDealGetEggsSerializer, DocumentsDeleteJsonSerializer, DocumentsGetFinanceSerializer, DocumentsGetPaymentsSerializer
)
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.services.base_deal.deal_services import finance_discipline_search, search_payments
from product_eggs.services.documents.docs_deleter import JsonDataDeleter
from product_eggs.services.documents.documents_srv import check_logic_UPD
from product_eggs.services.validation.check_validated_data import (
    check_val_data_contract_for_contract, check_val_data_contract_multy_pay,
    check_validated_data_for_tmp_json
)


class DocumentsViewSet(viewsets.ViewSet):
    """
    General view for two models,
    DocumentsDealEggsModel, DocumentsContractEggsModel.
    action path metod, for download pdf, save links, and edit statistic.
    """
    queryset = DocumentsDealEggsModel.objects.all()
    serializer_class = DocumentsDealEggsSerializer
    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])

    def get_deal_docs(self, request, pk=None) -> Response:
        serializer = DocumentsDealGetEggsSerializer(
            DocumentsDealEggsModel.objects.filter(pk=pk), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def patch_deal_docs(self, request, pk=None) -> Response:
        instance = DocumentsDealEggsModel.objects.get(pk=pk)
        serializer = DocumentsDealEggsSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if isinstance(serializer.validated_data, OrderedDict):
            check_validated_data_for_tmp_json(
                serializer.validated_data,
                instance,
                eq_requestuser_is_customuser(self.request.user)
            )
            check_logic_UPD(serializer.validated_data, request.data, instance)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def patch_docs_contract(self, request, pk=None) -> Response:
        instance = DocumentsContractEggsModel.objects.get(pk=pk)
        serializer = DocumentsContractEggsSerializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if isinstance(serializer.validated_data, OrderedDict):
            if check_val_data_contract_multy_pay(
                serializer.validated_data,
                instance,
                eq_requestuser_is_customuser(self.request.user)):
                return Response(status=status.HTTP_200_OK)
            if check_val_data_contract_for_contract(
                serializer.validated_data,
                instance):
                serializer.save()
                return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def remove_data_number_json(self, request, pk=None) -> Response:
        serializer = DocumentsDeleteJsonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if isinstance(serializer.validated_data, OrderedDict) and pk:
            delete_json = JsonDataDeleter(serializer.validated_data, pk, request.user)
            delete_json.main()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def get_clients_payments(self, request, pk=None) -> Response:
        serializer = DocumentsGetPaymentsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if isinstance(serializer.validated_data, OrderedDict):
            if search_data := search_payments(
                    serializer.validated_data['client_type'],
                    serializer.validated_data['cur_date']):
                serializer = BaseDealEggsGetPaymentsSerializer(search_data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def get_finance_discipline(self, request, pk=None) -> Response:
        serializer = DocumentsGetFinanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_serializers = {
            'seller': BaseDealEggsFinanceDisciplineSellerSerializer,
            'buyer': BaseDealEggsFinanceDisciplineBuyerSerializer,
            'logic': BaseDealEggsFinanceDisciplineLogicSerializer,
        }
        color_book = {
            'red': 0,
            'green': 0,
            'orange': 0,
        }
        if isinstance(serializer.validated_data, OrderedDict):
            if search_data := finance_discipline_search(
                    serializer.validated_data['client_type'],
                    serializer.validated_data['client_inn']):
                if serializer.validated_data['client_type'] in client_serializers.keys():
                    serializer = client_serializers[
                        serializer.validated_data['client_type']
                    ](search_data, many=True)
                else:
                    raise serializers.ValidationError('wrong client type in get_finance_discipline')

                for i in serializer.data:
                    try:
                        if i['finance_discipline']:
                            color_book[i['finance_discipline']] += 1
                    except TypeError:
                        pass

                return Response({'data': serializer.data, 'colors': color_book}, status=status.HTTP_200_OK)
            else:
                return Response({'data': [], 'colors': color_book}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)



