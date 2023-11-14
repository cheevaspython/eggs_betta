from rest_framework.response import Response
from rest_framework import views, permissions

from product_eggs.serializers.applications_serializers import ApplicationBuyerEggsSerializerSideBar,\
    ApplicationSellerEggsSerializerSideBar
from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.base_deal_serializers import CalculateEggsSerializerSideBar, \
    ConfirmedCalculateEggsSerializerSideBar, DealEggsSerializerSideBar


class LeftBarEggsViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer_current_user_app_buyer_eggs = ApplicationBuyerEggsSerializerSideBar(
            ApplicationFromBuyerBaseEggs.objects.filter(
                is_active=True, owner=self.request.user
            ).only('id'), many=True)
        serializer_current_user_app_selller_eggs = ApplicationSellerEggsSerializerSideBar(
            ApplicationFromSellerBaseEggs.objects.filter(
                is_active=True, owner=self.request.user
            ).only('id'), many=True)
        calcs_user_is_active = CalculateEggsSerializerSideBar(
            BaseDealEggsModel.objects.filter(
                is_active=True, owner=self.request.user, status=1,
            ).only('id', 'deal_buyer_pay_amount', 'deal_our_pay_amount', 'logic_our_pay_amount'),
            many=True)
        confirmed_calcs_user_is_active = ConfirmedCalculateEggsSerializerSideBar(
            BaseDealEggsModel.objects.filter(
                is_active=True, owner=self.request.user, status=2,
            ).only('id', 'deal_buyer_pay_amount', 'deal_our_pay_amount', 'logic_our_pay_amount'),
            many=True)
        deal_side_bar = DealEggsSerializerSideBar(
                BaseDealEggsModel.objects.only(
                    'id', 'documents_id', 'deal_our_pay_amount',
                    'deal_buyer_pay_amount', 'logic_our_pay_amount',
                    'is_active', 'status', 'owner_id'
                ), #.filter(Q(status=3) & Q(is_active=True) & Q(owner_id=self.request.user.pk)).annotate(
                #     new_id=F('documents_id'),
                #     model_id=F('id')).values('new_id', 'model_id'
                # ).annotate(id=F('new_id')).values('id', 'model_id'),
                many=True)

        return Response({
            'current_user_application_from_buyer_eggs': serializer_current_user_app_buyer_eggs.data,
            'current_user_application_from_seller_eggs': serializer_current_user_app_selller_eggs.data,
            'current_user_calculate_eggs': calcs_user_is_active.data,
            'current_user_confirmed_calculate_eggs': confirmed_calcs_user_is_active.data,
            'current_user_deal_eggs': deal_side_bar.data,
            })

