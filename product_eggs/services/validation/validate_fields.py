from string import ascii_lowercase, ascii_uppercase
from typing import OrderedDict

from django.utils.translation import gettext_lazy as _

from product_eggs.services.dates_check import validation_delivery_interval
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.validationerror import custom_error


def validate_charfield_for_letters(validate_data: str, error_type: str = 'serializer') -> None:
    """
    Проверяет данные на наличие букв (русский и английский алфавиты).
    """
    eng_alphabet = list(ascii_uppercase+ascii_lowercase)
    rus_alphabet = [chr(i) for i in range(ord('А'), ord('а') + 32)]

    if error_type == 'serializer':
        for symbol in validate_data:
            if symbol in rus_alphabet + eng_alphabet:
                raise custom_error('Никаких букв!')
    elif error_type == 'validator':
        for symbol in validate_data:
            if symbol in rus_alphabet + eng_alphabet:
                raise custom_error("ИНН должен состоять из цифр.")
    else:
        pass


def find_serializer_buyer_cost_data(validated_data: OrderedDict) -> None:
    """
    Проверяет данные на наличие полей с ценами на яйца.
    """
    try_check_validated_data_for_values(validated_data, 'cB_white_cost')
    try_check_validated_data_for_values(validated_data, 'cB_cream_cost')
    try_check_validated_data_for_values(validated_data, 'cB_brown_cost')
    try_check_validated_data_for_values(validated_data, 'c0_white_cost')
    try_check_validated_data_for_values(validated_data, 'c0_cream_cost')
    try_check_validated_data_for_values(validated_data, 'c0_brown_cost')
    try_check_validated_data_for_values(validated_data, 'c1_white_cost')
    try_check_validated_data_for_values(validated_data, 'c1_cream_cost')
    try_check_validated_data_for_values(validated_data, 'c1_brown_cost')
    try_check_validated_data_for_values(validated_data, 'c2_white_cost')
    try_check_validated_data_for_values(validated_data, 'c2_cream_cost')
    try_check_validated_data_for_values(validated_data, 'c2_brown_cost')
    try_check_validated_data_for_values(validated_data, 'c3_white_cost')
    try_check_validated_data_for_values(validated_data, 'c3_cream_cost')
    try_check_validated_data_for_values(validated_data, 'c3_brown_cost')
    try_check_validated_data_for_values(validated_data, 'dirt_cost')


@try_decorator_param(('KeyError', 'TypeError'))
def try_check_validated_data_for_values(validated_data, cost_data:str) -> None:
    """
    Проверка полей валидатором validate_charfield_for_letters.
    """
    validate_charfield_for_letters(validated_data[cost_data])


def validate_value_by_positive(value: float | int) -> None:
    """
    Проверка на положительное цисло (float).
    """
    if value <= 0:
        raise custom_error('Значение не может быть 0 или отрицательным')


@try_decorator_param(('KeyError', 'AttributeError'))
def validate_data_for_some_values(entry_data: OrderedDict, values: tuple) -> bool:
    """
    Проверка данных на компоненты tuple.
    """
    for value in values:
        entry_data[value]
    return True


def check_for_date_and_validate_them(serializer_data: OrderedDict) -> None:
    if validate_data_for_some_values(
            serializer_data, ('delivery_date_from_seller', 'delivery_date_to_buyer')):
        validation_delivery_interval(serializer_data['delivery_date_from_seller'],
            serializer_data['delivery_date_to_buyer'])
    else:
        raise custom_error('request error, не указаны -> delivery date!')


def validate_guest_role(value: str) -> None:
    """
    Проверка роли.
    """
    from users.models import CustomUser
    cur_user = CustomUser.objects.get(pk=value)
    if cur_user.role != '10':
        raise custom_error("Пользователь должен быть гостем.")


def validate_c1_to_dirt_count_box(value: str) -> None:
    """
    Проверка кратности коробки для категорий c1, c2, c3, грязь.
    """
    if value % 36:
        raise custom_error("Колличество должно быть кратно коробке (36 дес).")


def validate_c0_and_cB_count_box(value: str) -> None:
    """
    Проверка кратности коробки для категорий c0, cB.
    """
    if value % 30:
        raise custom_error("Колличество должно быть кратно коробке (30 дес).")


def validate_inn(value: str) -> None:
    """
    Валидация ИНН
    """
    if value.startswith('_'):
        validate_charfield_for_letters(value[1:], 'validator')
        if len(value) < 10 or len(value) > 13:
            raise custom_error("Колличество цифр должно быть в диапазоне 10-12")
    else:
        validate_charfield_for_letters(value, 'validator')
        if len(value) < 10 or len(value) > 12:
            raise custom_error("Колличество цифр должно быть в диапазоне 10-12")


def validate_for_letters(value: str) -> None:
    """
    Валидация цифр на наличие букв
    """
    eng_alphabet = list(ascii_uppercase+ascii_lowercase)
    rus_alphabet = [chr(i) for i in range(ord('А'), ord('а') + 32)]

    for symbol in value:
        if symbol in rus_alphabet + eng_alphabet:
            raise custom_error("В данном поле букв быть не должно.")

