from typing import OrderedDict

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.models.documents import DocumentsDealEggsModel, DocumentsContractEggsModel
from product_eggs.serializers.documents_serializers import DocumentsDealEggsSerializer, \
    DocumentsContractEggsSerializer, DocumentsDealGetEggsSerializer
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.services.documents.documents_srv import deal_docs_dict_json_update, \
    check_logic_UPD
from product_eggs.services.validation.check_validated_data import check_val_data_contract_for_contract,\
    check_val_data_contract_for_multy_pay, check_validated_data_for_tmp_json
from product_eggs.services.raw.documents import deal_docs_get_query


class DocumentsViewSet(viewsets.ViewSet):
    """
    General view for three models, 
    DocumentsDealEggsModel, DocumentsContractEggsModel, DocumentsBuyerEggsModel.
    action path metod, for download pdf, save links, and edit statistic.
    """
    queryset = DocumentsDealEggsModel.objects.all()
    serializer_class = DocumentsDealEggsSerializer

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_deal_docs(self, request, pk=None) -> Response:  
        serializer = DocumentsDealGetEggsSerializer(
            deal_docs_get_query(pk), many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def patch_deal_docs(self, request, pk=None) -> Response:
        instance = DocumentsDealEggsModel.objects.get(pk=pk)
        serializer = DocumentsDealEggsSerializer(instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            check_validated_data_for_tmp_json(
                serializer.validated_data,
                instance,
                eq_requestuser_is_customuser(self.request.user)
            )
            check_logic_UPD(serializer.validated_data, request.data, instance)
            deal_docs_dict_json_update(serializer.validated_data, 
                    eq_requestuser_is_customuser(self.request.user), instance)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)    

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def patch_docs_contract(self, request, pk=None) -> Response:
        instance = DocumentsContractEggsModel.objects.get(pk=pk)
        serializer = DocumentsContractEggsSerializer(instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):

            check_val_data_contract_for_multy_pay(
                serializer.validated_data,
                instance,
                eq_requestuser_is_customuser(self.request.user)
            )
            check_val_data_contract_for_contract(
                serializer.validated_data,
                instance
            )
        serializer.save()
            # instance.tmp_json_for_multi_pay_order = {}   #TODO
            # instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)    
