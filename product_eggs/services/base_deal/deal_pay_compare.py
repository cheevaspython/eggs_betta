import uuid
import logging
                
from rest_framework import serializers

from product_eggs.models.base_client import BuyerCardEggs, \
    LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.base_deal.deal_messages_payment import \
    construct_error_text, delta_compare_and_send_message, \
    delta_UPD_compare_and_send_message
from product_eggs.services.tails import add_tail_model_to_client


logger = logging.getLogger(__name__)


def compare_payment_and_inital_amount(
        instance: BaseDealEggsModel, 
        client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
        pay_amount: float,
        data_for_save: dict,
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

    if instance.__dict__[UPD_dict[client.__class__.__name__]]:
        #если УПД уже загружена
        delta = abs(instance.__dict__[pay_dict[client.__class__.__name__]]) - pay_amount

        if delta < 0:
            if data_for_save['force']:
                add_tail_model_to_client(client)
                instance.__dict__[pay_dict[client.__class__.__name__]] = 0
                data_for_save.pop('force', None)
                if instance.cash and isinstance(client, BuyerCardEggs | LogicCardEggs):
                    client.tails.current_tail_form_two += abs(delta)
                    client.tails.active_tails_form_two += 1
                    client.tails.tail_dict_json_cash.update(
                        {str(uuid.uuid4()): data_for_save})
                    client.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        pay_amount
                    )
                    return instance
                else:
                    client.tails.current_tail_form_one += abs(delta)
                    client.tails.active_tails_form_one += 1
                    client.tails.tail_dict_json.update(
                        {str(uuid.uuid4()): data_for_save})
                    client.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        pay_amount
                    )
                    return instance
            else:
                raise serializers.ValidationError(
                    construct_error_text(
                        instance.documents.pk,
                        text_client_dict[client.__class__.__name__][0],
                        instance.__dict__[UPD_dict[client.__class__.__name__]],
                        pay_amount, 
                        (instance.__dict__[UPD_dict[client.__class__.__name__]] - 
                            abs(instance.__dict__[pay_dict[client.__class__.__name__]])),
                        delta,
                        )
                    )
        else:
            delta_compare_and_send_message(
                delta,
                client,
                instance,
                text_client_dict[client.__class__.__name__][1],
                pay_amount
            )
            instance.__dict__[pay_dict[client.__class__.__name__]] += pay_amount
            return instance
    else:
        #если УПД не загружена, сравнение с суммой продукции (или примерной ценой доставки)
        #за вычетом пп 
        if isinstance(client, LogicCardEggs):
            inital_payments_amount = instance.delivery_cost
        elif isinstance(client, SellerCardEggs):
            inital_payments_amount = (
                instance.cB*instance.seller_cB_cost + instance.c0*instance.seller_c0_cost +
                instance.c1*instance.seller_c1_cost + instance.c2*instance.seller_c2_cost +
                instance.c3*instance.seller_c3_cost + instance.dirt*instance.seller_dirt_cost
            )
        elif isinstance(client, BuyerCardEggs):
            inital_payments_amount = (
                instance.cB*instance.buyer_cB_cost + instance.c0*instance.buyer_c0_cost +
                instance.c1*instance.buyer_c1_cost + instance.c2*instance.buyer_c2_cost +
                instance.c3*instance.buyer_c3_cost + instance.dirt*instance.buyer_dirt_cost
            )
        else:
            logging.warning('pay_service_wrong_inn_client, inital_amount = 0')
            inital_payments_amount = 0

        payments_sub = inital_payments_amount - \
            abs(instance.__dict__[pay_dict[client.__class__.__name__]]) 
        delta = payments_sub - pay_amount

        if delta < 0:
            if data_for_save['force']:
                add_tail_model_to_client(client)
                instance.__dict__[pay_dict[client.__class__.__name__]] = inital_payments_amount
                data_for_save.pop('force', None)
                if instance.cash and isinstance(client, BuyerCardEggs | LogicCardEggs):
                    client.tails.current_tail_form_two += abs(delta)
                    client.tails.active_tails_form_two += 1
                    client.tails.tail_dict_json_cash.update(
                        {str(uuid.uuid4()): data_for_save})
                    client.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        pay_amount
                    )
                    return instance
                else:
                    client.tails.current_tail_form_one += abs(delta)
                    client.tails.active_tails_form_one += 1
                    client.tails.tail_dict_json.update(
                        {str(uuid.uuid4()): data_for_save})
                    client.tails.save()
                    delta_compare_and_send_message(
                        delta,
                        client,
                        instance,
                        text_client_dict[client.__class__.__name__][1],
                        pay_amount
                    )
                    return instance
            else:
                raise serializers.ValidationError(
                    construct_error_text(
                        instance.documents.pk,
                        text_client_dict[client.__class__.__name__][2],
                        inital_payments_amount,
                        pay_amount, 
                        instance.__dict__[pay_dict[client.__class__.__name__]],
                        delta,
                        )
                    )
        else:
            delta_compare_and_send_message(
                delta,
                client,
                instance,
                text_client_dict[client.__class__.__name__][1],
                pay_amount
            )
            instance.__dict__[pay_dict[client.__class__.__name__]] += pay_amount
            return instance


def compare_UPD_and_payments(
        instance: BaseDealEggsModel,
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        data_for_save: dict,
        pay_amount: float) -> BaseDealEggsModel: 
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
    if instance.__dict__[UPD_dict[client.__class__.__name__]]:
        raise serializers.ValidationError(
            f"У сделки №{instance.documents.pk}, УПД уже загружен. " +
            "Проверьте введенные данные!"
        )
    else:
        delta = instance.__dict__[pay_dict[client.__class__.__name__]] - pay_amount
        instance.__dict__[UPD_dict[client.__class__.__name__]] = pay_amount

        if delta < 0:
            # недоплата, сумма по УПД больше, чем внесено. (может стать отрицательным)
            instance.__dict__[pay_dict[client.__class__.__name__]] = delta
            delta_UPD_compare_and_send_message(delta, client, instance)
            return instance

        elif delta > 0:
            # Переплата по УПД, разница в депозит.
            add_tail_model_to_client(client)
            instance.__dict__[pay_dict[client.__class__.__name__]] = 0
            if instance.cash:
                client.tails.current_tail_form_two += delta
                client.tails.active_tails_form_two += 1
                client.tails.tail_dict_json_cash.update(
                    {str(uuid.uuid4()): data_for_save})
                client.tails.save()
                delta_UPD_compare_and_send_message(delta, client, instance)
                return instance
            else:
                client.tails.current_tail_form_one += delta
                client.tails.active_tails_form_one += 1
                client.tails.tail_dict_json.update(
                    {str(uuid.uuid4()): data_for_save})
                client.tails.save()
                delta_UPD_compare_and_send_message(delta, client, instance)
                return instance
        else:
            # Внесенная сумма равна УПД.
            instance.__dict__[pay_dict[client.__class__.__name__]] = 0
            delta_UPD_compare_and_send_message(delta, client, instance)
            return instance
                        

