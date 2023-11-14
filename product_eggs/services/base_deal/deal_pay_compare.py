import uuid
import logging
from datetime import datetime
from dataclasses import asdict
from rest_framework import serializers

from product_eggs.models.base_client import (
    BuyerCardEggs, LogicCardEggs, SellerCardEggs
)
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.balance import get_cur_balance
from product_eggs.services.base_deal.deal_messages_payment import (
    construct_error_text, delta_compare_and_send_message,
    delta_UPD_send_message
)
from product_eggs.services.data_class.data_class_documents import PayOrderDataForSave
from product_eggs.services.tails import create_tail_model_to_balance

logger = logging.getLogger(__name__)


def compare_payment_and_inital_amount(
        instance: BaseDealEggsModel,
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        data_for_save: PayOrderDataForSave
        ) -> BaseDealEggsModel:
    """
    Сравнивает платежку и сумму сделки или УПД.
    Возвращает Измененную модель или ошибку.
    """
    pay_dict = {
        'SellerCardEggs': 'deal_our_pay_amount',
        'BuyerCardEggs': 'deal_buyer_pay_amount',
        'LogicCardEggs': 'logic_our_pay_amount',
    }
    UPD_dict = {
        'SellerCardEggs': 'deal_our_debt_UPD',
        'BuyerCardEggs': 'deal_buyer_debt_UPD',
        'LogicCardEggs': 'logic_our_debt_UPD',
    }
    text_client_dict = {
        'SellerCardEggs': ('по входящей УПД', 'продавцом', 'закупки'),
        'BuyerCardEggs': ('по исходящей УПД', 'покупателем', 'продажи'),
        'LogicCardEggs': ('перевозки', 'перевозчиком', 'перевозки'),
    }

    data_for_save_asdict = asdict(data_for_save)
    data_for_save_asdict.pop('force', None)

    if instance.entity:
        cur_balance = get_cur_balance(instance.entity, client)
    else:
        raise serializers.ValidationError(f'base deal: {instance.pk} field entity -> None! pay error')

    if instance.__dict__[UPD_dict[client.__class__.__name__]]:
        #если УПД уже загружена
        delta = abs(instance.__dict__[pay_dict[client.__class__.__name__]]) - data_for_save.pay_quantity

        if delta < 0:
            if data_for_save['force']:
                if not cur_balance.tails:
                    cur_balance.tails = create_tail_model_to_balance()
                    cur_balance.save()

                instance.__dict__[pay_dict[client.__class__.__name__]] = 0
                if instance.cash and isinstance(client, BuyerCardEggs):
                    cur_balance.tails.current_tail_form_two += abs(delta)
                    cur_balance.tails.active_tails_form_two += 1
                    cur_balance.tails.data_number_json_cash.update(
                        {str(uuid.uuid4()): data_for_save_asdict})
                    cur_balance.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        data_for_save.pay_quantity,
                        entity=data_for_save.entity,
                    )
                    return instance
                if instance.delivery_form_payment == 3 and isinstance(client, LogicCardEggs):
                    cur_balance.tails.current_tail_form_two += abs(delta)
                    cur_balance.tails.active_tails_form_two += 1
                    cur_balance.tails.data_number_json_cash.update(
                        {str(uuid.uuid4()): data_for_save_asdict})
                    cur_balance.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        data_for_save.pay_quantity,
                        entity=data_for_save.entity,
                    )
                    return instance
                else:
                    cur_balance.tails.current_tail_form_one += abs(delta)
                    cur_balance.tails.active_tails_form_one += 1
                    cur_balance.tails.data_number_json.update(
                        {str(uuid.uuid4()): data_for_save_asdict})
                    cur_balance.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        data_for_save.pay_quantity,
                        entity=data_for_save.entity,
                    )
                    return instance
            else:
                raise serializers.ValidationError(
                    construct_error_text(
                        instance.pk,
                        text_client_dict[client.__class__.__name__][0],
                        instance.__dict__[UPD_dict[client.__class__.__name__]],
                        data_for_save.pay_quantity,
                        (instance.__dict__[UPD_dict[client.__class__.__name__]] -
                            abs(instance.__dict__[pay_dict[client.__class__.__name__]])),
                        delta,
                        data_for_save.entity,
                        )
                    )
        else:
            delta_compare_and_send_message(
                delta,
                client,
                instance,
                text_client_dict[client.__class__.__name__][1],
                data_for_save.pay_quantity,
                entity=data_for_save.entity,
            )
            instance.__dict__[pay_dict[client.__class__.__name__]] += data_for_save.pay_quantity
            return instance
    else:
        #если УПД не загружена, сравнение с суммой продукции (или примерной ценой доставки)
        #за вычетом пп
        if isinstance(client, LogicCardEggs):
            inital_payments_amount = instance.delivery_cost
        elif isinstance(client, SellerCardEggs):
            inital_payments_amount = (
                instance.cB_white*instance.seller_cB_white_cost +
                instance.cB_cream*instance.seller_cB_cream_cost +
                instance.cB_brown*instance.seller_cB_brown_cost +
                instance.c0_white*instance.seller_c0_white_cost +
                instance.c0_cream*instance.seller_c0_cream_cost +
                instance.c0_brown*instance.seller_c0_brown_cost +
                instance.c1_white*instance.seller_c1_white_cost +
                instance.c1_cream*instance.seller_c1_cream_cost +
                instance.c1_brown*instance.seller_c1_brown_cost +
                instance.c2_white*instance.seller_c2_white_cost +
                instance.c2_cream*instance.seller_c2_cream_cost +
                instance.c2_brown*instance.seller_c2_brown_cost +
                instance.c3_white*instance.seller_c3_white_cost +
                instance.c3_cream*instance.seller_c3_cream_cost +
                instance.c3_brown*instance.seller_c3_brown_cost +
                instance.dirt*instance.seller_dirt_cost
            )
        elif isinstance(client, BuyerCardEggs):
            inital_payments_amount = (
                instance.cB_white*instance.buyer_cB_white_cost +
                instance.cB_cream*instance.buyer_cB_cream_cost +
                instance.cB_brown*instance.buyer_cB_brown_cost +
                instance.c0_white*instance.buyer_c0_white_cost +
                instance.c0_cream*instance.buyer_c0_cream_cost +
                instance.c0_brown*instance.buyer_c0_brown_cost +
                instance.c1_white*instance.buyer_c1_white_cost +
                instance.c1_cream*instance.buyer_c1_cream_cost +
                instance.c1_brown*instance.buyer_c1_brown_cost +
                instance.c2_white*instance.buyer_c2_white_cost +
                instance.c2_cream*instance.buyer_c2_cream_cost +
                instance.c2_brown*instance.buyer_c2_brown_cost +
                instance.c3_white*instance.buyer_c3_white_cost +
                instance.c3_cream*instance.buyer_c3_cream_cost +
                instance.c3_brown*instance.buyer_c3_brown_cost +
                instance.dirt*instance.buyer_dirt_cost
            )
        else:
            logging.warning('pay_service_wrong_inn_client, inital_amount = 0')
            inital_payments_amount = 0


        payments_sub = inital_payments_amount - \
            abs(instance.__dict__[pay_dict[client.__class__.__name__]])

        delta = payments_sub - data_for_save.pay_quantity

        if delta < 0:
            if data_for_save['force']:

                if not cur_balance.tails:
                    cur_balance.tails = create_tail_model_to_balance()
                    cur_balance.save()

                instance.__dict__[pay_dict[client.__class__.__name__]] = inital_payments_amount
                if instance.cash and isinstance(client, BuyerCardEggs):
                    cur_balance.tails.current_tail_form_two += abs(delta)
                    cur_balance.tails.active_tails_form_two += 1
                    cur_balance.tails.data_number_json_cash.update(
                        {str(uuid.uuid4()): data_for_save_asdict})
                    cur_balance.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        data_for_save.pay_quantity,
                        entity=data_for_save.entity,
                    )
                    return instance
                elif instance.delivery_form_payment == 3 and isinstance(client, LogicCardEggs):
                    cur_balance.tails.current_tail_form_two += abs(delta)
                    cur_balance.tails.active_tails_form_two += 1
                    cur_balance.tails.data_number_json_cash.update(
                        {str(uuid.uuid4()): data_for_save_asdict})
                    cur_balance.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        data_for_save.pay_quantity,
                        entity=data_for_save.entity,
                    )
                    return instance
                else:
                    cur_balance.tails.current_tail_form_one += abs(delta)
                    cur_balance.tails.active_tails_form_one += 1
                    cur_balance.tails.data_number_json.update(
                        {str(uuid.uuid4()): data_for_save_asdict})
                    cur_balance.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        data_for_save.pay_quantity,
                        entity=data_for_save.entity,
                    )
                    return instance
            else:
                raise serializers.ValidationError(
                    construct_error_text(
                        instance.pk,
                        text_client_dict[client.__class__.__name__][2],
                        inital_payments_amount,
                        data_for_save.pay_quantity,
                        instance.__dict__[pay_dict[client.__class__.__name__]],
                        delta,
                        data_for_save.entity,
                        )
                    )
        else:
            delta_compare_and_send_message(
                delta,
                client,
                instance,
                text_client_dict[client.__class__.__name__][1],
                data_for_save.pay_quantity,
                entity=data_for_save.entity,
            )
            instance.__dict__[pay_dict[client.__class__.__name__]] += data_for_save.pay_quantity
            return instance


def compare_UPD_and_payments(
        instance: BaseDealEggsModel,
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        data_for_save: PayOrderDataForSave
        ) -> BaseDealEggsModel:
    """
    Сравнивает сумму в УПД и сумму платежных поручений.
    """
    pay_dict = {
        'SellerCardEggs': 'deal_our_pay_amount',
        'BuyerCardEggs': 'deal_buyer_pay_amount',
        'LogicCardEggs': 'logic_our_pay_amount',
    }
    UPD_dict = {
        'SellerCardEggs': 'deal_our_debt_UPD',
        'BuyerCardEggs': 'deal_buyer_debt_UPD',
        'LogicCardEggs': 'logic_our_debt_UPD',
    }
    dates_dict = {
        'SellerCardEggs': 'actual_loading_date',
        'BuyerCardEggs': 'actual_unloading_date',
    }

    if instance.entity:
        cur_balance = get_cur_balance(instance.entity, client)
    else:
        raise serializers.ValidationError(f'base deal: {instance.pk} field entity -> None! pay error')

    if instance.__dict__[UPD_dict[client.__class__.__name__]]:
        raise serializers.ValidationError(
            f"У сделки №{instance.pk}, УПД уже загружен. " +
            "Проверьте введенные данные!"
        )
    else:
        delta = instance.__dict__[pay_dict[client.__class__.__name__]] - data_for_save.pay_quantity
        instance.__dict__[UPD_dict[client.__class__.__name__]] = data_for_save.pay_quantity

        #add actual dates from UPD
        if isinstance(client, BuyerCardEggs) or isinstance(client, SellerCardEggs):
            try:
                date_save = datetime.strptime(data_for_save.date,'%d/%m/%Y')
                instance.__dict__[dates_dict[client.__class__.__name__]] = date_save.strftime("%Y-%m-%d")
            except (TypeError, KeyError) as e:
                raise serializers.ValidationError('wrong date format in request', e)

        if delta < 0:
            # недоплата, сумма по УПД больше, чем внесено. (может стать отрицательным)
            instance.__dict__[pay_dict[client.__class__.__name__]] = delta
            text_val = 0
            delta_UPD_send_message(
                delta, text_val,
                client, instance,
                entity=data_for_save.entity
            )
            return instance

        elif delta > 0:
            # Переплата по УПД, разница в депозит.
            if not cur_balance.tails:
                cur_balance.tails = create_tail_model_to_balance()
                cur_balance.save()

            instance.__dict__[pay_dict[client.__class__.__name__]] = 0
            if instance.cash and isinstance(client, BuyerCardEggs):
                cur_balance.tails.current_tail_form_two += delta
                cur_balance.tails.active_tails_form_two += 1
                cur_balance.tails.data_number_json_cash.update(
                    {str(uuid.uuid4()): asdict(data_for_save)})
                cur_balance.tails.save()
                text_val = 2
                delta_UPD_send_message(
                    delta, text_val,
                    client, instance,
                    entity=data_for_save.entity
                )
                return instance

            elif instance.delivery_form_payment ==3 and isinstance(client, LogicCardEggs):
                cur_balance.tails.current_tail_form_two += delta
                cur_balance.tails.active_tails_form_two += 1
                cur_balance.tails.data_number_json_cash.update(
                    {str(uuid.uuid4()): asdict(data_for_save)})
                cur_balance.tails.save()
                text_val = 2
                delta_UPD_send_message(
                    delta, text_val,
                    client, instance,
                    entity=data_for_save.entity
                )
                return instance

            else:
                cur_balance.tails.current_tail_form_one += delta
                cur_balance.tails.active_tails_form_one += 1
                cur_balance.tails.data_number_json.update(
                    {str(uuid.uuid4()): asdict(data_for_save)})
                cur_balance.tails.save()
                text_val = 2
                delta_UPD_send_message(
                    delta, text_val,
                    client, instance,
                    entity=data_for_save.entity
                )
                return instance
        else:
            # Внесенная сумма равна УПД.
            instance.__dict__[pay_dict[client.__class__.__name__]] = 0
            text_val = 1
            delta_UPD_send_message(
                delta, text_val,
                client, instance,
                entity=data_for_save.entity
            )
            return instance


