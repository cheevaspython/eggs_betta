from product_eggs.permissions.validate_user import can_create_conf_anf_calc, can_edit_deal
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.validationerror import custom_error
from users.models import CustomUser


def check_create_deal_permission(user: CustomUser) -> None:
    if user not in can_create_conf_anf_calc():
        raise custom_error("У Вас нет прав для создания сделки")


def check_edit_deal_permission(user: CustomUser, instance: BaseDealEggsModel) -> None:
    can_edit_users_book = [
        instance.seller.manager,
        instance.buyer.manager,
        instance.owner
    ] + can_edit_deal()
    if user not in can_edit_users_book:
        raise custom_error("У Вас нет прав для редактирования сделки")


