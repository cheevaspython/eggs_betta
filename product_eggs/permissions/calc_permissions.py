from typing import OrderedDict

from django.db.models import Q
from rest_framework import serializers
from product_eggs.models.base_deal import BaseDealEggsModel

from product_eggs.permissions.validate_user import can_create_conf_anf_calc
from users.models import CustomUser


def check_create_calculate_user_permission(
            serializer_validated_data: OrderedDict, user: CustomUser) -> None:
    CURRENT_OWNERS = [
    #     serializer_validated_data['application_from_seller'].owner,
    #     serializer_validated_data['application_from_buyer'].owner
    ] 
    USERS_CAN_CREATE = list(CustomUser.objects.filter(Q(role=5) | Q(role=8)))

    if user not in CURRENT_OWNERS + USERS_CAN_CREATE:
        raise serializers.ValidationError(
            'У Вас нет прав для создания данного просчета')


def check_create_conf_calculate_user_permission(user: CustomUser) -> None:
    if user not in can_create_conf_anf_calc():
        raise serializers.ValidationError(
            "У Вас нет прав для подтверждения просчета")


def check_edit_calculate_permission(
        user: CustomUser, instance: BaseDealEggsModel) -> None:
    can_edit_users_book = [instance.seller, instance.buyer]
    USERS_CAN_EDIT = list(CustomUser.objects.filter(Q(role=5) | Q(role=8)))
     
    if user not in can_edit_users_book + USERS_CAN_EDIT:
        raise serializers.ValidationError(
            "У Вас нет прав для редактирования данного просчета")


def check_edit_conf_calculate_permission(user: CustomUser, instance) -> None:
    can_edit_users_book = [instance.seller, instance.buyer]
    USERS_CAN_EDIT = list(
        CustomUser.objects.filter(Q(role=4) | Q(role=5) | Q(role=8))
    )
    if user not in can_edit_users_book + USERS_CAN_EDIT:
        raise serializers.ValidationError(
            "У Вас нет прав для редактирования данного подтвержденного просчета")





