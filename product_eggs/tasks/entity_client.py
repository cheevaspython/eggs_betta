import logging
from collections import namedtuple
from celery import shared_task

from general_layout.balance.models.balance import BalanceBaseClient
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs

logger = logging.getLogger(__name__)


@shared_task
def change_client_entity_list(
        cur_balance_model: BalanceBaseClient,
        deleter: bool = False,
        ) -> None:
    """
    When BalanceBaseClientEggs created or deleted
    search all client balances
    save all active entitys
    """
    model_data = namedtuple(
            'model_fields', [
                'cur_client_model',
                'path_field',
            ]
    )
    from product_eggs.models.balance import BalanceBaseClientEggs

    if isinstance(cur_balance_model, BalanceBaseClientEggs):
        client_balance_book = {
            'buyer' : model_data(BuyerCardEggs, cur_balance_model.client_buyer),
            'seller' : model_data(SellerCardEggs, cur_balance_model.client_seller),
            'logic' : model_data(LogicCardEggs, cur_balance_model.client_logic),
        }
        if cur_balance_model.client_buyer:
            client_type = 'buyer'
        elif cur_balance_model.client_seller:
            client_type = 'seller'
        elif cur_balance_model.client_logic:
            client_type = 'logic'
        else:
            logger.debug(f'in balance model -> {cur_balance_model.pk} empty clients!')
            return

        entity = cur_balance_model.entity

        if deleter:
            if entity in client_balance_book[client_type].path_field.entitys.all():
                client_balance_book[client_type].path_field.entitys.remove(entity)

        else:
            if entity not in client_balance_book[client_type].path_field.entitys.all():
                client_balance_book[client_type].path_field.entitys.add(entity)

        client_balance_book[client_type].path_field.save()
    else:
        logger.debug(f'wrong balance type in shared_task : change_client_entity_list')
        return







