import logging

from django.core.exceptions import ObjectDoesNotExist

from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.models.base_client import (
    BuyerCardEggs, LogicCardEggs, SellerCardEggs
)
from product_eggs.models.entity import EntityEggs
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.decorators import try_decorator_param

logger = logging.getLogger(__name__)

entity_data = {
    'test': {
        'name': 'Пилигрим',
        'inn': 'test',
    },
    'test1': {
        'name': 'merc',
        'inn': 'test2',
    }
}


def get_new_balance_model(
        entity_inn: str,
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        ) -> BalanceBaseClientEggs:
    """
    Создает внешний ключ на модель баланса для клиента.
    default entity -> piligrim inn
    """
    if entity_inn not in entity_data.keys():
        raise KeyError('wrong entity inn in get_new_balance_model')

    client_seller=None
    client_buyer=None
    client_logic=None
    entity_model = EntityEggs.objects.get_or_create(
        inn=entity_data[entity_inn]['inn'],
        name=entity_data[entity_inn]['name'],
    )

    match client.__class__.__name__:
        case 'BuyerCardEggs':
            client_buyer = client
        case 'SellerCardEggs':
            client_seller = client
        case 'LogicCardEggs':
            client_logic = client
        case _:
            logging.debug('wrong client type in services/balance.py -> get_new_balance_model')
    new_balance = BalanceBaseClientEggs.objects.create(
        pay_limit=5000000,
        pay_limit_cash=5000000,
        entity=entity_model[0],
        client_seller=client_seller,
        client_buyer=client_buyer,
        client_logic=client_logic,
    )
    new_balance.save()
    return  new_balance


def get_cur_balance(
        entity: str | EntityEggs,
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
        ) -> BalanceBaseClientEggs:
    """
    get current balace or create new
    """
    if isinstance(entity, EntityEggs):
        entity_inn = entity.inn
    elif isinstance(entity, str):
        entity_inn = entity_data[entity]['inn']
    elif entity == None:
        raise KeyError('entity data == None, in get_cur_balance')

    if all_balances := client.cur_balance.all():
        for cur_balance in all_balances:
            if cur_balance.entity.inn == entity_inn:
                return cur_balance

    return get_new_balance_model(entity_inn, client)


def get_balance_for_tail(cur_tail: TailsContragentModelEggs) -> BalanceBaseClientEggs:
    result = BalanceBaseClientEggs.objects.get(tails=cur_tail)
    return result


@try_decorator_param(('ValueError',))
def get_balance_for_tail_pk(cur_tail_pk: int) -> BalanceBaseClientEggs:
    result = BalanceBaseClientEggs.objects.get(tails_id=cur_tail_pk)
    return result


def add_balance_to_client_if_havent(entity_inn: str, client: BuyerCardEggs | SellerCardEggs | LogicCardEggs) -> None:
    try:
        if client.cur_balance.get(entity=entity_inn):
            pass
    except ObjectDoesNotExist:
        get_new_balance_model(entity_inn, client)











