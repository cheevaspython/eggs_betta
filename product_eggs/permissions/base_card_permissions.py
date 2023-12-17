from product_eggs.permissions.validate_user import (
    can_create_logiccard, can_create_sellercard_or_buyercard
)
from product_eggs.services.validationerror import custom_error
from users.models import CustomUser


def check_create_base_card_user_permission(user: CustomUser) -> None:
    if user not in can_create_sellercard_or_buyercard():
        raise custom_error("У Вас нет прав для создания базы клиентов")


def check_create_base_card_user_permission_for_logic(user: CustomUser) -> None:
    if user not in can_create_logiccard():
        raise custom_error("У Вас нет прав для создания базы клиентов")

