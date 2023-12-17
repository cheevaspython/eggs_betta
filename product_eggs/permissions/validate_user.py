from typing import Any

from django.db.models import Q
from rest_framework.request import Request
from product_eggs.services.validationerror import custom_error

from users.models import CustomUser


def eq_requestuser_is_customuser(requestuser: CustomUser | Any) -> CustomUser:
    if isinstance(requestuser, CustomUser):
        return requestuser
    else:
        raise custom_error('Request user is not Customuser', 433)


def validate_user_for_statistic_page_change(request: Request) -> None:
    PERMISSION_ACCEESS_TO_STATISTIC = list(CustomUser.objects.filter(Q(role=6) |
        Q(role=7) | Q(role=8)))
    if request.user not in PERMISSION_ACCEESS_TO_STATISTIC:
            raise custom_error('Permission denied', 435)


def validate_user_for_statistic_page_list(request: Request) -> None:
    PERMISSION_ACCEESS_TO_STATISTIC = list(CustomUser.objects.filter(Q(role=6) |
        Q(role=1) | Q(role=2) | Q(role=3) | Q(role=5) | Q(role=7) | Q(role=8)))
    if request.user not in PERMISSION_ACCEESS_TO_STATISTIC:
        raise custom_error('Permission denied', 435)


def validate_user_for_statistic_page_list_logic(request: Request) -> None:
    PERMISSION_ACCEESS_TO_STATISTIC = list(CustomUser.objects.filter(Q(role=6) |
        Q(role=1) | Q(role=2) | Q(role=3) | Q(role=4) | Q(role=5) | Q(role=7) | Q(role=8)))
    if request.user not in PERMISSION_ACCEESS_TO_STATISTIC:
        raise custom_error('Permission denied', 435)


def can_create_conf_anf_calc() -> list[CustomUser]:
    CAN_CREATE_CONFCALC_AND_DEAL = list(CustomUser.objects.filter(Q(role=5) |
        Q(role=6) | Q(role=8)))
    return CAN_CREATE_CONFCALC_AND_DEAL


def can_create_sellercard_or_buyercard() -> list[CustomUser]:
    CAN_CREATE_CLIENTCARD = list(CustomUser.objects.filter(Q(role=6) | Q(role=8) | Q(role=5) | Q(role=4)))
    return CAN_CREATE_CLIENTCARD


def can_create_logiccard() -> list[CustomUser]:
    CAN_CREATE_CLIENTCARD = list(CustomUser.objects.filter(Q(role=6) | Q(role=4) | Q(role=8) | Q(role=5)))
    return CAN_CREATE_CLIENTCARD


def can_edit_deal() -> list[CustomUser]:
    CAN_EDIT_DEAL = list(CustomUser.objects.filter(
        Q(role=6) | Q(role=8) | Q(role=5) | Q(role=7) | Q(role=4)))
    return CAN_EDIT_DEAL


def can_edit_deal_super_user() -> list[CustomUser]:
    CAN_EDIT_DEAL = list(CustomUser.objects.filter(
        Q(role=5) | Q(role=6) | Q(role=8)))
    return CAN_EDIT_DEAL


def super_users_and_buh_book() -> list[CustomUser]:
    SUPER_USERS_AND_BUH = list(CustomUser.objects.filter(Q(role=6) | Q(role=7) | Q(role=8)))
    return SUPER_USERS_AND_BUH


def verificate_user_as_superuser(user: CustomUser) -> bool:
	return True if user in can_edit_deal() else False

