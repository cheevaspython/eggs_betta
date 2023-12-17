from rest_framework import permissions, status
from rest_framework.response import Response

from product_eggs.models.comment import CommentEggs
from product_eggs.serializers.applications_serializers import (
    ApplicationBuyerEggsDetailSerializer, ApplicationSellerEggsDetailSerializer
)
from product_eggs.models.applications import (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
)
from product_eggs.services.dates_check import validate_datas_for_positive_app, validation_delivery_interval
from product_eggs.models.custom_model_viewset import CustomModelViewSet
from product_eggs.permissions.apps_permission import (
    USER_ROLES_SUPER, check_create_buyer_application_user_permission,
    check_create_seller_application_user_permission, check_edit_application_user_permission
)
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from users.models import CustomUser


class ApplicationSellerEggsViewSet(CustomModelViewSet):
    queryset = ApplicationFromSellerBaseEggs.objects.all().select_related(
        'current_seller', 'owner').select_related(
        'current_seller__requisites', 'current_seller__documents_contract'
    ).prefetch_related('current_seller__contact_person')
    serializer_class = ApplicationSellerEggsDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        check_create_seller_application_user_permission(
            serializer.validated_data,
            eq_requestuser_is_customuser(self.request.user)
        )
        serializer.validated_data['owner'] = self.request.user

        if isinstance(self.request.user, CustomUser):
            if self.request.user.role in USER_ROLES_SUPER:
                pass
            else:
                validation_delivery_interval(
                    serializer.validated_data['delivery_window_from'],
                    serializer.validated_data['delivery_window_until'],
                )
        new_comment_model = CommentEggs.objects.create()
        new_comment_model.save()
        serializer.validated_data['comment_json'] = new_comment_model
        serializer.save()

    def list(self, request, *args, **kwargs):
        applications_seller_is_active = ApplicationFromSellerBaseEggs.objects.filter(is_active=True).select_related(
            'current_seller', 'owner', 'comment_json',
            'current_seller__requisites', 'current_seller__documents_contract',
            'current_seller__manager',
        ).prefetch_related(
            'current_seller__contact_person', 'current_seller__cur_balance'
        )
        page = self.paginate_queryset(applications_seller_is_active)
        if page is not None:
            serializer = ApplicationSellerEggsDetailSerializer(
                applications_seller_is_active, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ApplicationSellerEggsDetailSerializer(
            applications_seller_is_active, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if isinstance(self.request.user, CustomUser):
            if self.request.user.role in USER_ROLES_SUPER:
                pass
            else:
                validate_datas_for_positive_app(serializer.validated_data)
        self.perform_update(serializer, instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(status=status.HTTP_200_OK)

    def perform_update(self, serializer, instance):
        check_edit_application_user_permission(
            eq_requestuser_is_customuser(self.request.user),
            instance,
        )
        serializer.save()


class ApplicationBuyerEggsViewSet(CustomModelViewSet):
    queryset = ApplicationFromBuyerBaseEggs.objects.all().select_related(
        'current_buyer', 'owner').select_related(
        'current_buyer__requisites', 'current_buyer__documents_contract'
    ).prefetch_related('current_buyer__contact_person')
    serializer_class = ApplicationBuyerEggsDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        check_create_buyer_application_user_permission(
            serializer.validated_data,
            eq_requestuser_is_customuser(self.request.user),
        )
        serializer.validated_data['owner'] = self.request.user
        if isinstance(self.request.user, CustomUser):
            if self.request.user.role in USER_ROLES_SUPER:
                pass
            else:
                validation_delivery_interval(
                    serializer.validated_data['delivery_window_from'],
                    serializer.validated_data['delivery_window_until'],
                )
        new_comment_model = CommentEggs.objects.create()
        new_comment_model.save()
        serializer.validated_data['comment_json'] = new_comment_model
        serializer.save()

    def list(self, request, *args, **kwargs):
        applications_buyer_is_active = ApplicationFromBuyerBaseEggs.objects.filter(
            is_active=True
        ).select_related(
            'current_buyer', 'owner', 'current_buyer__manager', 'comment_json',
            'current_buyer__requisites', 'current_buyer__documents_contract'
        ).prefetch_related('current_buyer__contact_person', 'current_buyer__cur_balance')
        page = self.paginate_queryset(applications_buyer_is_active)
        if page is not None:
            serializer = ApplicationBuyerEggsDetailSerializer(
                applications_buyer_is_active, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ApplicationBuyerEggsDetailSerializer(
            applications_buyer_is_active, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if isinstance(self.request.user, CustomUser):
            if self.request.user.role in USER_ROLES_SUPER:
                pass
            else:
                validate_datas_for_positive_app(serializer.validated_data)
        self.perform_update(serializer, instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response(status=status.HTTP_200_OK)

    def perform_update(self, serializer, instance):
        check_edit_application_user_permission(
            eq_requestuser_is_customuser(self.request.user), instance)
        serializer.save()

