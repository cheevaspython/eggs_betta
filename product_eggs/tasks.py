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
