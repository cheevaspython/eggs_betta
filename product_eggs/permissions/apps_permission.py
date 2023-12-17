from typing import OrderedDict, Union

from django.db.models import Q

from product_eggs.models.applications import (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
)
from product_eggs.services.validationerror import custom_error
from users.models import CustomUser

USER_ROLES_SUPER = ['5', '6', '8']


def check_create_seller_application_user_permission(
        serializer_validated_data: OrderedDict, user: CustomUser
    ) -> None:
    SELLER_MANAGER = [serializer_validated_data['current_seller'].manager]
    SELLER_GUEST = [serializer_validated_data['current_seller'].guest]
    USERS_CAN_CREATE = list(CustomUser.objects.filter(Q(role=5) | Q(role=1) | Q(role=3) | Q(role=8)))

    if user not in SELLER_MANAGER + SELLER_GUEST + USERS_CAN_CREATE:
        raise custom_error('У Вас нет прав для создания данной заявки')


def check_create_buyer_application_user_permission(
        serializer_validated_data: OrderedDict, user: CustomUser) -> None:
    BUYER_MANAGER = [serializer_validated_data['current_buyer'].manager]
    BUYER_GUEST = [serializer_validated_data['current_buyer'].guest]
    USERS_CAN_CREATE = list(CustomUser.objects.filter(Q(role=5) | Q(role=2) | Q(role=3)  | Q(role=8)))

    if user not in BUYER_MANAGER + BUYER_GUEST + USERS_CAN_CREATE:
        raise custom_error('У Вас нет прав для создания данной заявки')


def check_edit_application_user_permission(
        user: CustomUser,
        instance: Union[ApplicationFromSellerBaseEggs, ApplicationFromBuyerBaseEggs]) -> None:
    OWNER = [instance.owner]
    USERS_CAN_EDIT = list(CustomUser.objects.filter(Q(role=5) | Q(role=8)))

    if user not in USERS_CAN_EDIT + OWNER:
        raise custom_error("У Вас нет прав для редактирования данной заявки")
