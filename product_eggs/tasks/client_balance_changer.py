from celery import shared_task



@shared_task
def change_client_balance_tail(tail_id: int) -> None:
    # from product_eggs.services.get_anything.try_to_get_models import \  TODO
    #     get_client_for_tail_pk
    from product_eggs.services.balance import get_balance_for_tail_pk
    """
    Task changed Client balance, then change
    tail balance.
    """
    cur_balance = get_balance_for_tail_pk(tail_id)
    if cur_balance:
        cur_balance.save()
    # client = get_client_for_tail_pk(tail_id)
    # if client:
    #     client.save()
