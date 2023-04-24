from celery import shared_task
from product_eggs.models.base_client import AbstractClientCard
                                                                            
                                                                                                       
@shared_task
def change_client_balance_deal(client: AbstractClientCard,
        delta: float, cash: bool) -> None:
    """
    Task changed Client balance, then change
    deal balance.
    """
    from product_eggs.models.base_client import SellerCardEggs, BuyerCardEggs
    
    if isinstance(client, SellerCardEggs | BuyerCardEggs):
        if cash:
            client.balance_form_two += delta
        else:
            client.balance_form_one += delta
        client.save()
    else:
        print('error in task, wrong inn')


@shared_task
def change_client_balance_tail(tail_id: int) -> None:
    from product_eggs.services.get_anything.try_to_get_models import get_client_for_tail_pk
    """
    Task changed Client balance, then change
    tail balance.
    """
    client = get_client_for_tail_pk(tail_id)
    if client:
        client.save()
