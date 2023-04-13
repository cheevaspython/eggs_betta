from rest_framework import serializers

from product_eggs.permissions.validate_user import can_create_conf_anf_calc, can_edit_deal
from product_eggs.models.base_deal import BaseDealEggsModel
from users.models import CustomUser


def check_create_deal_permission(user: CustomUser) -> None:
    if user not in can_create_conf_anf_calc():
        raise serializers.ValidationError("У Вас нет прав для создания сделки")


def check_edit_deal_permission(user: CustomUser, instance: BaseDealEggsModel) -> None:
    can_edit_users_book = [instance.seller, instance.buyer] + can_edit_deal()
    if user not in can_edit_users_book:
        raise serializers.ValidationError("У Вас нет прав для редактирования сделки")


