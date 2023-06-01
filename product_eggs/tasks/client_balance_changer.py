from celery import shared_task
            
            
@shared_task
def change_client_balance_tail(tail_id: int) -> None:
    from product_eggs.services.get_anything.try_to_get_models import \
        get_client_for_tail_pk
    """
    Task changed Client balance, then change
    tail balance.
    """
    client = get_client_for_tail_pk(tail_id)
    if client:
        client.save()
