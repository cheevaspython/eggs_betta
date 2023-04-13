from typing import Optional

from product_eggs.services.message_send_save import create_send_and_save_message, \
     send_message_to_users_queryset_conf_calculate_model, \
     send_message_to_users_queryset_calculate_model
from product_eggs.models.calcs_deal_eggs import CalculateEggs, ConfirmedCalculateEggs
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs, LogicCardEggs
from users.models import CustomUser


def message_calculate_create(current_calc: CalculateEggs) -> None:
    send_message_to_users_queryset_calculate_model(
        f'Создан новый просчет №{current_calc.pk}',
        current_calc,
        CustomUser.objects.filter(role=5))


def message_calc_confirmed(current_conf_calc: ConfirmedCalculateEggs) -> None:
    create_send_and_save_message(
        f'Просчет №{current_conf_calc.current_calculate.pk} подтвержден',
        current_conf_calc.current_calculate.owner,
        conf_calculate = current_conf_calc)


def message_conf_cal_to_logic(current_conf_calc: ConfirmedCalculateEggs) -> None:
    send_message_to_users_queryset_conf_calculate_model(
        f'Подтвержденный просчет №{current_conf_calc.pk} создан и ожидает добавления перевозчика',
        current_conf_calc,
        CustomUser.objects.filter(role=4))


def send_message_note_to_calc_owner(
        note: str, instance: CalculateEggs | ConfirmedCalculateEggs) -> None:
    if isinstance(instance, ConfirmedCalculateEggs):
        create_send_and_save_message(
            f'Замечание по подтвержденному просчету №{instance.pk}: \n {note}',
            instance.current_calculate.owner,
            conf_calculate = instance
        )
    else:
        create_send_and_save_message(
            f'Замечание по просчету №{instance.pk}: \n {note}',
            instance.owner,
            calculate = instance
        )


def send_message_to_finance_director(
        message: str, 
        instance: Optional[BuyerCardEggs | SellerCardEggs | LogicCardEggs]) -> None:

    if isinstance(instance, BuyerCardEggs):
        create_send_and_save_message(
            message,
            CustomUser.objects.get(role=6),
            buyer = instance
        )
    elif isinstance(instance, SellerCardEggs):
        create_send_and_save_message(
            message,
            CustomUser.objects.get(role=6),
            seller = instance
        )
    elif isinstance(instance, LogicCardEggs):
        create_send_and_save_message(
            message,
             CustomUser.objects.get(role=6),
            logic = instance
        )
    else:
        print('instance in send_message to fin dir invalid')

