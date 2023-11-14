from rest_framework import serializers

from product_eggs.permissions.validate_user import (
    can_create_logiccard, can_create_sellercard_or_buyercard
)
from users.models import CustomUser


def check_create_base_card_user_permission(user: CustomUser) -> None:
    if user not in can_create_sellercard_or_buyercard():
        raise serializers.ValidationError("У Вас нет прав для создания базы клиентов")


def check_create_base_card_user_permission_for_logic(user: CustomUser) -> None:
    if user not in can_create_logiccard():
        raise serializers.ValidationError("У Вас нет прав для создания базы клиентов")

