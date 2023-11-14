from product_eggs.models.base_client import (
    BuyerCardEggs, LogicCardEggs, SellerCardEggs
)
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.entity import EntityEggs
from product_eggs.services.data_class.data_class import TailDataForJsonSave
from product_eggs.services.data_class.data_class_documents import PayOrderDataForSave, PayOrderDataForSaveMultiClear
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from users.models import CustomUser


def delta_compare_and_send_message(
        delta: float,
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        instance: BaseDealEggsModel,
        payment_type: str,
        pay_amount: float,
        entity: str) -> None:
    """
    Формирует сообщение в зависимости от параметра дельта.
    """
    entity_name = EntityEggs.objects.get(pk=entity).name
    if delta == 0:
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            construct_close_debt_text(
                instance.pk,
                payment_type,
                client,
                pay_amount,
                entity_name,
            )
        )
        message.send_message()
    elif delta > 0:
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            construct_close_partly_debt_text(
                instance.pk,
                payment_type,
                client,
                pay_amount,
                delta,
                entity_name,
            )
        )
        message.send_message()
    else:
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            construct_tail_text(
                instance.pk,
                client,
                delta,
                pay_amount,
                entity_name,
            )
        )
        message.send_message()


def delta_UPD_send_message(
        delta: float,
        text_val: int,
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        instance: BaseDealEggsModel,
        entity: str,
        ) -> None:
    """
    Формирует сообщение в зависимости от параметра дельта.
    """
    TEXT_VALUES = [0, 1, 2]
    if text_val not in TEXT_VALUES:
        raise ValueError('wrong text_val in pay_compare')
    entity_name = EntityEggs.objects.get(pk=entity).name
    message = MessageLibrarrySend(
        'message_to_finance_director',
        instance,
        construct_UPD_text(
            delta,
            text_val,
            instance.pk,
            client,
            entity_name,
        )
    )
    message.send_message()


def construct_UPD_text(
        delta: float,
        text_val: int,
        deal_pk: int,
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        entity_name: str) -> str:
    """
    Формирует сообщение фин. директору по входящей УПД.
    """
    name_dict = {
        'BuyerCardEggs': 'продавца',
        'SellerCardEggs': 'для покупателя',
        'LogicCardEggs': 'перевозчика',
    }
    text_tuple = (
        f'больше, чем внесено платежей на данный момент. Остается внести - {abs(delta)} ₽.',
        'равна сумме платежей.',
        'меньше чем сумма внесенных платежей, остаток будет переведен в баланс клиента.',
    )
    return(
        f"<<{entity_name}>> По сделке №{deal_pk} загруженна УПД от " +
        f"{name_dict[client.__class__.__name__]}: " +
        f"{client}, сумма в УПД {text_tuple[text_val]} ₽."
    )


def construct_error_text(
        deal_pk: int,
        payment_type: str,
        tmp_limit: float,
        pay_amount: float,
        already_enrolled: float,
        delta: float,
        entity: str) -> str:
    """
    Формирует сообщение ошибки.
    """
    entity_name = EntityEggs.objects.get(pk=entity).name
    if already_enrolled:
        enrolled = f"уже зачислено - {abs(already_enrolled)} ₽."
    else:
        enrolled = ''
    return(
        f"<<{entity_name}>> У сделки №{deal_pk}, сумма {payment_type} составляет " +
        f"- {abs(tmp_limit)} ₽., {enrolled}. " +
        f"Вы вностите {pay_amount}, разница составляет " +
        f"{abs(delta)} ₽., проверьте данные!")


def construct_close_debt_text(
        deal_pk: str, payment_type: str,
        pay_client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
        pay_amount: float,
        entity_name: str) -> str:
    """
    Формирует сообщение при закрытии долга.
    """
    return(
        f"<<{entity_name}>> По сделке №{deal_pk} - долг перед {payment_type} закрыт. " +
        f"ПП от {pay_client} на сумму {round(pay_amount, 2)} ₽.")


def construct_tail_text(
        deal_pk,
        pay_client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
        delta: float,
        pay_amount: float,
        entity_name: str) -> str:
    """
    Формирует сообщение при закрытии долга.
    """
    if isinstance(pay_client, BuyerCardEggs | LogicCardEggs):
        to = 'от'
    else:
        to = 'для'
    return(
        f"<<{entity_name}>> По сделке №{deal_pk} внесен ПП {to} {pay_client} " +
        f"на сумму {round(pay_amount, 2)} ₽. {round(abs(delta), 2)} ₽. " +
        f"отправленно на баланс контрагента.")


def construct_close_partly_debt_text(
        deal_pk, payment_type: str,
        pay_client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
        pay_amount: float,
        delta: float,
        entity_name: str) -> str:
    """
    Формирует сообщение при внесении платежного поручения,
    возвращает разницу.
    """
    return(
        f"<<{entity_name}>> ПП от {pay_client} по сделке №{deal_pk}, " +
        f"на сумму {pay_amount} ₽. внесен, остаток долга " +
        f"перед {payment_type} составляет - {abs(delta)} ₽.")


def data_num_json_canceled_send_message(
        data_number: PayOrderDataForSave | PayOrderDataForSaveMultiClear | TailDataForJsonSave,
        client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
        cancel_user: CustomUser) -> None:
    """
    Формирует сообщение при удалении.
    """
    if isinstance(data_number, PayOrderDataForSave):
        instance = BaseDealEggsModel.objects.get(pk=data_number.deal)
        entity_name = EntityEggs.objects.get(pk=data_number.entity).name
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            f"<<{entity_name}>> Документ от {client} по сделке №{instance.pk}, под номером {data_number.number}, " +
            f"на сумму {data_number.pay_quantity} ₽. отменен пользователем {cancel_user}.",
        )
        message.send_message()

    elif isinstance(data_number, PayOrderDataForSaveMultiClear):
        entity_name = EntityEggs.objects.get(pk=data_number.entity).name
        message = MessageLibrarrySend(
            'message_to_finance_director',
            client,
            f"<<{entity_name}>> Документ от {client}, под номером {data_number.number}, " +
            f"на сумму {data_number.total_amount} ₽. отменен пользователем {cancel_user}.",
        )
        message.send_message()

    elif isinstance(data_number, TailDataForJsonSave):
        entity_name = EntityEggs.objects.get(pk=data_number.entity).name
        message = MessageLibrarrySend(
            'message_to_finance_director',
            client,
            f"<<{entity_name}>> Документ от {client}, под номером {data_number.number}, " +
            f"на сумму {data_number.pay_quantity} ₽. отменен пользователем {cancel_user}.",
        )
        message.send_message()









