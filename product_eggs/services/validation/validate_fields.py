from string import ascii_lowercase, ascii_uppercase
from typing import OrderedDict

from rest_framework import serializers

from product_eggs.services.dates_check import validation_delivery_interval
from product_eggs.services.decorators import try_decorator_param


def validate_charfield_for_letters(validate_data: str) -> None:
    """
    Проверяет данные на наличие букв (русский и английский алфавиты).
    """
    eng_alphabet = list(ascii_uppercase+ascii_lowercase)
    rus_alphabet = [chr(i) for i in range(ord('А'), ord('а') + 32)]
    
    for symbol in validate_data:
        if symbol in rus_alphabet + eng_alphabet:
            raise serializers.ValidationError('Никаких букв!')


def find_serializer_buyer_cost_data(validated_data: OrderedDict) -> None:
    """
    Проверяет данные на наличие полей с ценами на яйца.
    """
    try_check_validated_data_for_values(validated_data, 'cB_cost')
    try_check_validated_data_for_values(validated_data, 'c0_cost')
    try_check_validated_data_for_values(validated_data, 'c1_cost')
    try_check_validated_data_for_values(validated_data, 'c2_cost')
    try_check_validated_data_for_values(validated_data, 'c3_cost')
    try_check_validated_data_for_values(validated_data, 'dirt_cost')


@try_decorator_param(('KeyError', 'TypeError'))
def try_check_validated_data_for_values(validated_data, cost_data:str) -> None:
    """
    Проверка полей валидатором validate_charfield_for_letters. 
    """
    validate_charfield_for_letters(validated_data[cost_data])


def validate_value_by_positive(value:float) -> None:
    """
    Проверка на положительное цисло (float). 
    """
    if value <= 0:
        raise serializers.ValidationError('Значение не может быть 0 или отрицательным')


@try_decorator_param(('KeyError', 'AttributeError'))
def validate_data_for_some_values(entry_data: OrderedDict, values: tuple) -> bool:
    for value in values:
        entry_data[value]
    return True


def check_for_date_and_validate_them(serializer_data: OrderedDict) -> None:
    if validate_data_for_some_values(
            serializer_data, ('delivery_date_from_seller', 'delivery_date_to_buyer')):
        validation_delivery_interval(serializer_data['delivery_date_from_seller'], 
            serializer_data['delivery_date_to_buyer'])
    else:
        raise serializers.ValidationError('request error, date not in request!')






