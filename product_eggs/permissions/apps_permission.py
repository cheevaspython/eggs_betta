from typing import OrderedDict, Union

from django.db.models import Q
from rest_framework import serializers

from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from users.models import CustomUser


def check_create_seller_application_user_permission(
        serializer_validated_data: OrderedDict, user: CustomUser) -> None:
    SELLER_MANAGER = [serializer_validated_data['current_seller'].manager] 
    USERS_CAN_CREATE = list(CustomUser.objects.filter(Q(role=5) | Q(role=8)))

    if user not in SELLER_MANAGER + USERS_CAN_CREATE:
        raise serializers.ValidationError('У Вас нет прав для создания данной заявки')


def check_create_buyer_application_user_permission(
        serializer_validated_data: OrderedDict, user: CustomUser) -> None:
    BUYER_MANAGER = [serializer_validated_data['current_buyer'].manager] 
    USERS_CAN_CREATE = list(CustomUser.objects.filter(Q(role=5) | Q(role=8)))

    if user not in BUYER_MANAGER + USERS_CAN_CREATE:
        raise serializers.ValidationError('У Вас нет прав для создания данной заявки')


def check_edit_application_user_permission(
        user: CustomUser,
        instance: Union[ApplicationFromSellerBaseEggs, ApplicationFromBuyerBaseEggs]) -> None:
    OWNER = [instance.owner] 
    USERS_CAN_EDIT = list(CustomUser.objects.filter(Q(role=5) | Q(role=8)))

    if user not in USERS_CAN_EDIT + OWNER:
        raise serializers.ValidationError("У Вас нет прав для редактирования данной заявки")
