from django.db.models import F, Q
from rest_framework import views, permissions

from product_eggs.serializers.applications_serializers import (
    ApplicationBuyerEggsSerializerSideBar, ApplicationSellerEggsSerializerSideBar
)
from product_eggs.models.applications import (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
)
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.base_deal_serializers import (
    CalculateEggsSerializerSideBar, ConfirmedCalculateEggsSerializerSideBar,
    DealEggsSerializerSideBar
)


class LeftBarEggsViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
            serializer_current_user_app_buyer_eggs = ApplicationBuyerEggsSerializerSideBar(
                ApplicationFromBuyerBaseEggs.objects.select_related(
                    'current_buyer'
                ).filter(Q(is_active=True) & Q(owner_id=request.user.pk)).annotate(
                    name=F('current_buyer__requisites__name')
            ).values('id', 'is_actual', 'await_add_cost', 'name'), many=True)

            serializer_current_user_app_selller_eggs = ApplicationSellerEggsSerializerSideBar(
                ApplicationFromSellerBaseEggs.objects.select_related(
                    'current_seller'
                ).filter(Q(is_active=True) & Q(owner_id=request.user.pk)).annotate(
                    name=F('current_seller__requisites__name')
            ).values('id', 'is_actual', 'await_add_cost', 'name'), many=True)

            calcs_user_is_active = CalculateEggsSerializerSideBar(
                BaseDealEggsModel.objects.select_related(
                    'buyer', 'seller', 'owner'
                ).filter(Q(status=1) & Q(is_active=True) & Q(owner_id=request.user.pk)).annotate(
                    seller_name_orm=F('seller__requisites__name'),
                    buyer_name_orm=F('buyer__requisites__name')
                ).values(
                    'id', 'documents_id', 'deal_our_pay_amount',
                    'deal_buyer_pay_amount', 'logic_our_pay_amount',
                    'is_active', 'status', 'owner_id', 'seller_name_orm', 'buyer_name_orm',
                ), many=True)

            confirmed_calcs_user_is_active = ConfirmedCalculateEggsSerializerSideBar(
                BaseDealEggsModel.objects.select_related(
                    'buyer', 'seller', 'owner'
                ).filter(Q(status=2) & Q(is_active=True) & Q(owner_id=request.user.pk)).annotate(
                    seller_name_orm=F('seller__requisites__name'),
                    buyer_name_orm=F('buyer__requisites__name')
                ).values(
                    'id', 'documents_id', 'deal_our_pay_amount',
                    'deal_buyer_pay_amount', 'logic_our_pay_amount',
                    'is_active', 'status', 'owner_id', 'seller_name_orm', 'buyer_name_orm',
                ), many=True)

            deal_side_bar = DealEggsSerializerSideBar(
                BaseDealEggsModel.objects.select_related(
                    'buyer', 'seller', 'owner'
                ).filter(Q(status=3) & Q(is_active=True) & Q(owner_id=request.user.pk)).annotate(
                    seller_name_orm=F('seller__requisites__name'),
                    buyer_name_orm=F('buyer__requisites__name')
                ).values(
                    'id', 'documents_id', 'deal_our_pay_amount',
                    'deal_buyer_pay_amount', 'logic_our_pay_amount', 'deal_status',
                    'is_active', 'status', 'owner_id', 'seller_name_orm', 'buyer_name_orm',
                ), many=True)

            resp_data = {
                'current_user_application_from_buyer_eggs': serializer_current_user_app_buyer_eggs.data,
                'current_user_application_from_seller_eggs': serializer_current_user_app_selller_eggs.data,
                'current_user_calculate_eggs': calcs_user_is_active.data,
                'current_user_confirmed_calculate_eggs': confirmed_calcs_user_is_active.data,
                'current_user_deal_eggs': deal_side_bar.data,
            }
            return resp_data
