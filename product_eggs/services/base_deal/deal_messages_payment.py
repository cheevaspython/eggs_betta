from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, \
    SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.messages.messages_library import MessageLibrarrySend


def delta_compare_and_send_message(
        delta: float, 
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        instance: BaseDealEggsModel,
        payment_type: str,
        pay_amount) -> None:
    """
    Формирует сообщение в зависимости от параметра дельта.
    """
    if delta == 0:
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            construct_close_debt_text(
                instance.documents.pk,
                payment_type, client, 
                pay_amount,
            )
        )
        message.send_message()
    elif delta > 0:
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            construct_close_partly_debt_text(
                instance.documents.pk,
                payment_type, client, 
                pay_amount,
                delta,
            )
        )
        message.send_message()
    else:
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            construct_tail_text(
                instance.documents.pk,
                client, 
                delta,
                pay_amount,
            )
        )
        message.send_message()


def delta_UPD_compare_and_send_message(
        delta: float, 
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        instance: BaseDealEggsModel
        ) -> None:
    """
    Формирует сообщение в зависимости от параметра дельта.
    """
    if delta == 0:
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            construct_UPD_text(
                delta,
                1,
                instance.documents.pk,
                client,
            )
        )
        message.send_message()

    elif delta > 0:
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            construct_UPD_text(
                delta,
                2,
                instance.documents.pk,
                client,
            )
        )
        message.send_message()

    else:
        message = MessageLibrarrySend(
            'message_to_finance_director',
            instance,
            construct_UPD_text(
                delta,
                0,
                instance.documents.pk,
                client,
            )
        )
        message.send_message()


def construct_UPD_text(
        delta: float,
        text_val: int,
        deal_pk: int,
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs) -> str:
    """
    Формирует сообщение фин. директору по входящей УПД.
    """
    name_dict = {
        'BuyerCardEggs': 'продавца',  
        'SellerCardEggs': 'нас для покупателя',
        'LogicCardEggs': 'перевозчика',
    }
    text_tuple = (
        f'больше, чем внесено платежей на данный момент. Остается внести - {abs(delta)}',
        'равна сумме платежей.',
        'меньше чем сумма внесенных платежей, остаток будет переведен в баланс клиента.',
    )
    return(
        f"По сделке №{deal_pk} загруженна УПД от " + 
        f"{name_dict[client.__class__.__name__]}: " + 
        f"{client}/{client.pk}, сумма в УПД {text_tuple[text_val]}." 
    )


def construct_error_text(
        deal_pk: int,
        payment_type: str,
        tmp_limit: float,
        pay_amount: float,
        already_enrolled: float,
        delta: float) -> str:
    """
    Формирует сообщение ошибки.
    """
    if already_enrolled:
        enrolled = f"уже зачислено - {abs(already_enrolled)} ₽."
    else:
        enrolled = ''
    return(
        f"У сделки №{deal_pk}, сумма {payment_type} составляет " +
        f"- {abs(tmp_limit)} ₽., {enrolled}. " +
        f"Вы вностите {pay_amount}, разница составляет " +
        f"{abs(delta)} ₽., проверьте данные!")


def construct_close_debt_text(
        deal_pk, payment_type: str,
        pay_client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
        pay_amount: float) -> str:
    """
    Формирует сообщение при закрытии долга.
    """
    return(
        f"По сделке №{deal_pk} - долг перед {payment_type} закрыт. " + 
        f"ПП от {pay_client}/{pay_client.pk} на сумму {round(pay_amount, 2)} ₽.")


def construct_tail_text(
        deal_pk,
        pay_client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
        delta: float,
        pay_amount: float) -> str:
    """
    Формирует сообщение при закрытии долга.
    """
    if isinstance(pay_client, BuyerCardEggs | LogicCardEggs):
        to = 'от'
    else:
        to = 'для'
    return(
        f"По сделке №{deal_pk} внесен ПП {to} {pay_client}/{pay_client.pk} " + 
        f"на сумму {round(pay_amount, 2)} ₽. {round(abs(delta), 2)} ₽. " +
        f"отправленно на баланс контерагента.")


def construct_close_partly_debt_text(
        deal_pk, payment_type: str,
        pay_client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
        pay_amount: float, delta: float) -> str:
    """
    Формирует сообщение при внесении платежного поручения,
    возвращает разницу.
    """
    return(
        f"ПП от {pay_client}/{pay_client.pk} по сделке №{deal_pk}, " +
        f"на сумму {pay_amount} ₽. внесен, остаток долга " +
        f"перед {payment_type} составляет - {abs(delta)} ₽.")

