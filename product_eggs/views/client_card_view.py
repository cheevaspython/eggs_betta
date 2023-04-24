from rest_framework import permissions

from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs, LogicCardEggs
from product_eggs.models.documents import DocumentsContractEggsModel 
from product_eggs.permissions.base_card_permissions import check_create_base_card_user_permission
from product_eggs.services.requisites import create_requisites_model
from product_eggs.serializers.base_client_serializers import SellerCardEggsDetailSerializer, \
    BuyerCardEggsDetailSerializer, LogicCardEggsDetailSerializer, RequisitesDetailSerializer
from product_eggs.models.custom_model_viewset import CustomModelViewSet
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser


class SellerCardEggsViewSet(CustomModelViewSet):
    permission_classes = [permissions.IsAuthenticated]   
    queryset = SellerCardEggs.objects.all().select_related('requisites', 'documents_contract')
    serializer_class = SellerCardEggsDetailSerializer

    def perform_create(self, serializer):
        check_create_base_card_user_permission(
            eq_requestuser_is_customuser(self.request.user))
        req_serializer = RequisitesDetailSerializer(data=self.request.data)
        req_serializer.is_valid()
        new_requisites = create_requisites_model(req_serializer.data) 
        serializer.save()

        current_seller = self.queryset.get(inn=serializer.data['inn'])
        current_seller.documents_contract = DocumentsContractEggsModel.objects.create()
        current_seller.requisites = new_requisites
        current_seller.save()


class BuyerCardEggsViewSet(CustomModelViewSet):
    permission_classes = [permissions.IsAuthenticated]   
    queryset = BuyerCardEggs.objects.all().select_related('requisites', 'documents_contract')
    serializer_class = BuyerCardEggsDetailSerializer

    def perform_create(self, serializer):
        check_create_base_card_user_permission(
            eq_requestuser_is_customuser(self.request.user))
        req_serializer = RequisitesDetailSerializer(data=self.request.data)
        req_serializer.is_valid()
        new_requisites = create_requisites_model(req_serializer.data) 
        serializer.save()  

        current_buyer = self.queryset.get(inn=serializer.data['inn'])
        current_buyer.documents_contract = DocumentsContractEggsModel.objects.create()
        current_buyer.requisites = new_requisites
        current_buyer.save()


class LogicCardEggsViewSet(CustomModelViewSet):
    permission_classes = [permissions.IsAuthenticated]   
    queryset = LogicCardEggs.objects.all().select_related('requisites')
    serializer_class = LogicCardEggsDetailSerializer

    def perform_create(self, serializer):
        check_create_base_card_user_permission(
            eq_requestuser_is_customuser(self.request.user))
        req_serializer = RequisitesDetailSerializer(data=self.request.data)
        req_serializer.is_valid()
        new_requisites = create_requisites_model(req_serializer.data) 
        serializer.save()

        current_logic = self.queryset.get(inn=serializer.data['inn'])
        current_logic.documents_contract = DocumentsContractEggsModel.objects.create()
        current_logic.requisites = new_requisites
        current_logic.save()
