from datetime import date
from typing import OrderedDict

from rest_framework import serializers

from product_eggs.services.decorators import try_decorator_param


def validation_date_for_positive(date: date) -> None:
    """
    Проверка даты на настоящую, если нет, raise exception.
    """
    if date < date.today():
        raise serializers.ValidationError('Дата не может быть прошедшей!')


def validation_delivery_interval(delivery_window_from: date, delivery_window_until: date) -> None:
    """
    Проверка дат на порядок (дата погрузки должна быть раньше даты разгрузки).
    Проверяет интервал вводимых дат, окна поставки. Окно не должно превышать месяц.
    """
    validation_date_for_positive(delivery_window_from)
    delta = delivery_window_until - delivery_window_from
    if delivery_window_until < delivery_window_from:
        raise serializers.ValidationError('Дата разгрузки не может быть раньше даты погрузки!')
    if delta.days > 30:
        raise serializers.ValidationError('Окно доставки более месяца')


@try_decorator_param(('AttributeError','KeyError',))
def validate_datas_for_positive(validate_data: OrderedDict) -> None:
    """
    Проверяет вводимые даты CalculateEggs модели на настоящие.
    """
    validation_date_for_positive(validate_data['delivery_date_from_seller'])
    validation_date_for_positive(validate_data['delivery_date_to_buyer'])


@try_decorator_param(('AttributeError','KeyError',))
def validate_datas_for_positive_app(validate_data: OrderedDict) -> None:
    """
    Проверяет вводимые даты CalculateEggs модели на настоящие.
    """
    validation_date_for_positive(validate_data['delivery_window_from'])
    validation_date_for_positive(validate_data['delivery_window_until'])
