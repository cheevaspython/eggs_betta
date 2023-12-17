from collections import namedtuple

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.custom_model_viewset import CustomModelViewSet
from product_eggs.models.documents import DocumentsContractEggsModel
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.permissions.base_card_permissions import check_create_base_card_user_permission
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.serializers.base_client_serializers import (
    BuyerCardEggsDetailSerializer, LogicCardEggsDetailSerializer,
    SellerCardEggsDetailSerializer
)
from product_eggs.serializers.documents_serializers import DocumentsContractEggsSerializer
from product_eggs.serializers.requisites_serializers import RequisitesEggsModelSerializer
from product_eggs.services.validationerror import custom_error


class RequisitesModelViewSet(CustomModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RequisitesEggs.objects.all()
    serializer_class = RequisitesEggsModelSerializer
    http_method_names = ['get', 'post', 'patch']

    def perform_create_client(self, serializer):
        check_create_base_card_user_permission(
            eq_requestuser_is_customuser(self.request.user))
        serializer.validated_data['documents_contract'] = DocumentsContractEggsModel.objects.create()

        try:
            serializer.validated_data['requisites'] = \
                RequisitesEggs.objects.get(inn=serializer.validated_data['inn'])
        except ObjectDoesNotExist as e:
            raise custom_error(f'reqisites with current inn does not exists {e}', 433)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    @transaction.atomic
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def patch_multi_request(self, request, pk=None) -> Response:
        if pk:
            parse_pk = pk.replace('-', ' ').split()
            models_data = namedtuple(
                    'model_and_serializer', [
                        'cur_client_model',
                        'cur_client_serializer',
                    ]
            )
            clients_book = {
                'buyer' : models_data(BuyerCardEggs, BuyerCardEggsDetailSerializer),
                'seller' : models_data(SellerCardEggs, SellerCardEggsDetailSerializer),
                'logic' : models_data(LogicCardEggs, LogicCardEggsDetailSerializer),
            }
            instance_requisites = RequisitesEggs.objects.filter(pk=parse_pk[0]).first()
            if instance_requisites:
                serializer_requisites = RequisitesEggsModelSerializer(
                    instance_requisites, data=request.data, partial=True)
                serializer_requisites.is_valid(raise_exception=True)
            else:
                serializer_requisites = self.get_serializer(data=request.data)
                serializer_requisites.is_valid(raise_exception=True)
                self.perform_create(serializer_requisites)
                instance_requisites = RequisitesEggs.objects.filter(pk=parse_pk[0]).first()

            instance_client = clients_book[parse_pk[1]].cur_client_model.objects.filter(pk=parse_pk[0]).first()
            if instance_client:
                serializer_client = clients_book[parse_pk[1]].cur_client_serializer(
                    instance_client, data=request.data, partial=True)
                serializer_client.is_valid(raise_exception=True)
            else:
                serializer_client = clients_book[parse_pk[1]].cur_client_serializer(data=request.data)
                serializer_client.is_valid(raise_exception=True)
                self.perform_create_client(serializer_client)
                instance_client = clients_book[parse_pk[1]].cur_client_model.objects.filter(pk=parse_pk[0]).first()

            if instance_client:
                instance_documents = DocumentsContractEggsModel.objects.get(
                    pk=instance_client.documents_contract.pk
                )
                serializer_documents = DocumentsContractEggsSerializer(
                    instance_documents, data=request.data, partial=True)
                serializer_documents.is_valid(raise_exception=True)

                serializer_requisites.save() # fix n+1 save
                serializer_client.save()
                serializer_documents.save()
                response_data = {
                    'client_data': serializer_client.data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                raise custom_error('Error in get client after create', 433)

        return Response(status=status.HTTP_400_BAD_REQUEST)





