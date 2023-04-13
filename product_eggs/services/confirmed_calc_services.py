from collections import OrderedDict

from rest_framework import serializers

from product_eggs.models.calcs_deal_eggs import ConfirmedCalculateEggs
from product_eggs.models.base_eggs import LogicCardEggs
from product_eggs.services.create_expense_model import expense_model_creator
from product_eggs.services.message_send_save import send_message_to_users_queryset_conf_calculate_model, \
        create_send_and_save_message
from users.models import CustomUser
                 

def check_fields_values_to_calc_ready(current_conf_calc: ConfirmedCalculateEggs) -> None:
    conf_calc_fields = (current_conf_calc.current_logic,
        current_conf_calc.delivery_date_from_seller,
        current_conf_calc.delivery_date_to_buyer,
        current_conf_calc.delivery_cost,
        current_conf_calc.logic_confirmed,
    )
    for item in conf_calc_fields:
        if item is None or False:
            current_conf_calc.calc_ready = False
            current_conf_calc.save()
            raise serializers.ValidationError(f'Для продолжения заполните {item}')


def check_calc_ready_for_true(conf_calc: ConfirmedCalculateEggs) -> None: 
    if conf_calc.calc_ready:
        raise serializers.ValidationError('Просчет уже на подтверждении!')


def create_related_conf_calc_and_additional_expense(instance: ConfirmedCalculateEggs) -> None:
    if instance.additional_expense is None:
        instance.additional_expense = expense_model_creator()
        instance.save()   
    else:
        return print('additional_expense not None')


def check_fields_calc_ready_send_message(instance: ConfirmedCalculateEggs) -> None:
    check_fields_values_to_calc_ready(instance)
    send_message_to_users_queryset_conf_calculate_model(
            f'Одобрите подтвержденный просчет №{instance.pk} для перехода в статус Сделка.',
        instance, CustomUser.objects.filter(role=5))


def add_fields_to_conf_calc_if_delivery_by_seller(instance: ConfirmedCalculateEggs) -> None:
    if instance.current_calculate.delivery_by_seller:
        instance.logic_confirmed = True
        instance.current_logic = LogicCardEggs.objects.get(id=1)
        instance.save()
        send_message_to_calc_owner_logic_confirmed(instance)


def send_message_if_logic_confirmed(serializer_data: OrderedDict, instance: ConfirmedCalculateEggs) -> None:
    if serializer_data['logic_confirmed']:
            send_message_to_calc_owner_logic_confirmed(instance)


def send_message_to_calc_owner_logic_confirmed(instance: ConfirmedCalculateEggs) -> None:
    message = (f'Логист добавлен в подтвержденный просчет №{instance.pk}, \
            готов к отправке на подтверждение менеджеру направления')
    calc_owner = instance.current_calculate.owner
    create_send_and_save_message(message, calc_owner, conf_calculate=instance)



