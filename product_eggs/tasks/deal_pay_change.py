import logging
from celery import shared_task

from product_eggs.models.base_client import AbstractClientCard

logger = logging.getLogger(__name__)


@shared_task
def change_client_balance_deal(client: AbstractClientCard,
        delta: float, cash: bool) -> None:
    """                                             
    Task changed Client balance, then change
    deal balance.
    """
    from product_eggs.models.base_client import \
        SellerCardEggs, BuyerCardEggs, LogicCardEggs

    if isinstance(client, SellerCardEggs):
        client.balance_form_one += delta
        client.save()
    elif isinstance(client, BuyerCardEggs | LogicCardEggs):
        if cash:
            client.balance_form_two += delta
            client.save()
        else:
            client.balance_form_one += delta
            client.save()
    else:
        logging.warning('task error (calc deal)')
