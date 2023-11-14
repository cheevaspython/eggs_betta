from django.core.exceptions import ObjectDoesNotExist

from rest_framework import permissions, serializers, status, filters
from rest_framework.response import Response

from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs, LogicCardEggs
from product_eggs.models.documents import DocumentsContractEggsModel
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.permissions.base_card_permissions import (
    check_create_base_card_user_permission, check_create_base_card_user_permission_for_logic
)
from product_eggs.serializers.base_client_serializers import (
    BuyerCardEggsPlusRequisitesSerializer, SellerCardEggsDetailSerializer,
    BuyerCardEggsDetailSerializer, LogicCardEggsDetailSerializer,
    SellerCardEggsPlusRequisitesSerializer
)
from product_eggs.models.custom_model_viewset import CustomModelViewSet, CustomModelPagination
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from users.models import CustomUser


class ClientCardModelView(CustomModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomModelPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['requisites__name', 'inn']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        check_create_base_card_user_permission(
            eq_requestuser_is_customuser(self.request.user))
        serializer.validated_data['documents_contract'] = DocumentsContractEggsModel.objects.create()

        try:
            serializer.validated_data['requisites'] = \
                RequisitesEggs.objects.get(inn=serializer.validated_data['inn'])
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError('reqisites with current inn does not exists', e)
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SellerCardEggsViewSet(ClientCardModelView):
    queryset = SellerCardEggs.objects.all().select_related(
        'requisites', 'documents_contract',
        'manager', 'guest',
    ).prefetch_related('contact_person', 'cur_balance',)
    serializer_class = SellerCardEggsDetailSerializer


class BuyerCardEggsViewSet(ClientCardModelView):
    queryset = BuyerCardEggs.objects.all().select_related(
        'requisites', 'documents_contract',
        'manager', 'guest',
    ).prefetch_related('contact_person', 'cur_balance',)
    serializer_class = BuyerCardEggsDetailSerializer


class LogicCardEggsViewSet(ClientCardModelView):
    queryset = LogicCardEggs.objects.all().select_related(
        'requisites', 'documents_contract',
        'manager', 'guest',
    ).prefetch_related('contact_person', 'cur_balance',)
    serializer_class = LogicCardEggsDetailSerializer

    def perform_create(self, serializer):
        check_create_base_card_user_permission_for_logic(
            eq_requestuser_is_customuser(self.request.user))
        serializer.validated_data['documents_contract'] = DocumentsContractEggsModel.objects.create()

        try:
            serializer.validated_data['requisites'] = \
                RequisitesEggs.objects.get(inn=serializer.validated_data['inn'])
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError('reqisites with current inn does not exists', e)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class GetUserCardEggsViewSet(CustomModelViewSet):
    queryset = SellerCardEggs.objects.all()
    serializer_class = SellerCardEggsPlusRequisitesSerializer
    http_method_names = ['get']

    def list(self, request, *args, **kwargs) -> Response:
        if isinstance(self.request.user, CustomUser):
            if self.request.user.role == '10':
                seller_queryset = SellerCardEggs.objects.filter(guest=self.request.user)
                buyer_queryset = BuyerCardEggs.objects.filter(guest=self.request.user)
            else:
                seller_queryset = SellerCardEggs.objects.filter(manager=self.request.user)
                buyer_queryset = BuyerCardEggs.objects.filter(manager=self.request.user)
        else:
            return Response('Check entry data or user', status=status.HTTP_200_OK)

        seller_serializer = SellerCardEggsPlusRequisitesSerializer(seller_queryset, many=True)
        buyer_serializer = BuyerCardEggsPlusRequisitesSerializer(buyer_queryset, many=True)
        return Response({'sellers': seller_serializer.data, 'buyers': buyer_serializer.data}, status=status.HTTP_200_OK)


