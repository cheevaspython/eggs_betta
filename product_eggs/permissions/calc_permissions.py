from typing import OrderedDict

from django.db.models import Q

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.permissions.validate_user import can_create_conf_anf_calc
from product_eggs.services.validationerror import custom_error
from users.models import CustomUser


def check_create_calculate_user_permission(
        serializer_validated_data: OrderedDict, user: CustomUser) -> None:
    CURRENT_OWNERS = [
        ApplicationFromSellerBaseEggs.objects.get(pk=serializer_validated_data['application_from_seller']).owner,
        ApplicationFromBuyerBaseEggs.objects.get(pk=serializer_validated_data['application_from_buyer']).owner,
    ]
    USERS_CAN_CREATE = list(CustomUser.objects.filter(Q(role=5) | Q(role=8)))

    if user not in USERS_CAN_CREATE + CURRENT_OWNERS:
        raise custom_error(
            'У Вас нет прав для создания данного просчета')


def check_create_conf_calculate_user_permission(user: CustomUser) -> None:
    if user not in can_create_conf_anf_calc():
        raise custom_error(
            "У Вас нет прав для подтверждения просчета")


def check_edit_calculate_permission(
        user: CustomUser, instance: BaseDealEggsModel) -> None:
    can_edit_users_book = [instance.seller.manager, instance.buyer.manager]
    USERS_CAN_EDIT = list(CustomUser.objects.filter(Q(role=5) | Q(role=8)))

    if user not in can_edit_users_book + USERS_CAN_EDIT:
        raise custom_error(
            "У Вас нет прав для редактирования данного просчета")


def check_edit_conf_calculate_permission(user: CustomUser, instance: BaseDealEggsModel) -> None:
    can_edit_users_book = [instance.seller.manager, instance.buyer.manager]
    USERS_CAN_EDIT = list(
        CustomUser.objects.filter(Q(role=4) | Q(role=5) | Q(role=8))
    )
    if user not in can_edit_users_book + USERS_CAN_EDIT:
        raise custom_error(
            "У Вас нет прав для редактирования данного подтвержденного просчета")





