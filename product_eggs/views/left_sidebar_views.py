from rest_framework.response import Response
from rest_framework import views, permissions

from product_eggs.serializers.apps_serializers_eggs import ApplicationBuyerEggsSerializerSideBar,\
    ApplicationSellerEggsSerializerSideBar
from product_eggs.serializers.calc_deal_serializers_eggs import CalculateEggsSerializerSideBar, \
    ConfirmedCalculateEggsSerializerSideBar, DealEggsSerializerSideBar
from product_eggs.models.apps_eggs import ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
from product_eggs.models.calcs_deal_eggs import CalculateEggs, ConfirmedCalculateEggs, DealEggs


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
            CalculateEggs.objects.filter(
                is_active=True, owner=self.request.user
            ).only('id'), many=True) 
        confirmed_calcs_user_is_active = ConfirmedCalculateEggsSerializerSideBar(
            ConfirmedCalculateEggs.objects.filter(
                is_active=True, owner=self.request.user
            ).only('id'), many=True) 
        deal_user_is_active = DealEggsSerializerSideBar(
            DealEggs.objects.filter(
                is_active=True, owner=self.request.user
            ).only('id'), many=True) 

        return Response({
            'current_user_application_from_buyer_eggs': serializer_current_user_app_buyer_eggs.data, 
            'current_user_application_from_seller_eggs': serializer_current_user_app_selller_eggs.data,
            'current_user_calculate_eggs': calcs_user_is_active.data,
            'current_user_confirmed_calculate_eggs': confirmed_calcs_user_is_active.data,
            'current_user_deal_eggs': deal_user_is_active.data,
            })



