from rest_framework import response, permissions

from product_eggs.serializers.apps_serializers_eggs import ApplicationBuyerEggsDetailSerializer, \
    ApplicationSellerEggsDetailSerializer
from product_eggs.models.apps_eggs import ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
from product_eggs.services.dates_check import validation_delivery_interval
from product_eggs.models.custom_model_viewset import CustomModelViewSet
from product_eggs.permissions.apps_permission import check_create_buyer_application_user_permission, \
    check_create_seller_application_user_permission, check_edit_application_user_permission
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser


class ApplicationSellerEggsViewSet(CustomModelViewSet):  
    queryset = ApplicationFromSellerBaseEggs.objects.all().select_related('current_seller', 'owner').\
        select_related('current_seller__requisites', 'current_seller__documents_contract') 
    serializer_class = ApplicationSellerEggsDetailSerializer
    permission_classes = [permissions.IsAuthenticated]   

    def perform_create(self, serializer):
        check_create_seller_application_user_permission(
            serializer.validated_data, eq_requestuser_is_customuser(self.request.user))
        serializer.validated_data['owner'] = self.request.user    
        validation_delivery_interval(serializer.validated_data['delivery_window_from'], \
            serializer.validated_data['delivery_window_until'])
        serializer.save()

    def list(self, request, *args, **kwargs):
        applications_seller_is_active = ApplicationFromSellerBaseEggs.objects.filter(is_active=True).select_related(
            'current_seller', 'owner').select_related('current_seller__requisites', 'current_seller__documents_contract') 
        page = self.paginate_queryset(applications_seller_is_active)
        if page is not None:
            serializer = ApplicationSellerEggsDetailSerializer(applications_seller_is_active, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ApplicationSellerEggsDetailSerializer(applications_seller_is_active, many=True)
        return response.Response(serializer.data)
    
    def perform_update(self, serializer, instance):
        check_edit_application_user_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        serializer.save()


class ApplicationBuyerEggsViewSet(CustomModelViewSet):      
    queryset = ApplicationFromBuyerBaseEggs.objects.all().select_related('current_buyer', 'owner').\
        select_related('current_buyer__requisites', 'current_buyer__documents_contract') 
    serializer_class = ApplicationBuyerEggsDetailSerializer
    permission_classes = [permissions.IsAuthenticated]   

    def perform_create(self, serializer):
        check_create_buyer_application_user_permission(
            serializer.validated_data, eq_requestuser_is_customuser(self.request.user))
        serializer.validated_data['owner'] = self.request.user
        validation_delivery_interval(serializer.validated_data['delivery_window_from'], \
            serializer.validated_data['delivery_window_until'])
        serializer.save()

    def list(self, request, *args, **kwargs):
        applications_buyer_is_active = ApplicationFromBuyerBaseEggs.objects.filter(is_active=True).select_related(
            'current_buyer', 'owner').select_related('current_buyer__requisites', 'current_buyer__documents_contract') 
        page = self.paginate_queryset(applications_buyer_is_active)
        if page is not None:
            serializer = ApplicationBuyerEggsDetailSerializer(applications_buyer_is_active, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ApplicationBuyerEggsDetailSerializer(applications_buyer_is_active, many=True)
        return response.Response(serializer.data)

    def perform_update(self, serializer, instance):
        check_edit_application_user_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        serializer.save()

