from datetime import datetime

from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs
from product_eggs.models.tails import TailsContragentModelEggs


def add_tail_model_to_client(client: BuyerCardEggs | SellerCardEggs) -> None:
    """
    if client dont have related tail
    create new tail model and save 
    """
    if client.tails:
        pass
    else:
        new_tail = TailsContragentModelEggs.objects.create()
        new_tail.save()
        client.tails = new_tail
        client.save()


def tails_treatment(
        multy_pay_dict: dict,
        client: BuyerCardEggs | SellerCardEggs) -> None:
    """
    add deposit in form
    add count tails
    save model
    """
    add_tail_model_to_client(client)

    if multy_pay_dict['tail_form_one']:
        client.tails.current_tail_form_one += multy_pay_dict['tail_form_one'] 
        client.tails.active_tails_form_one += 1
        multy_pay_dict.pop('tail_form_two', None)
        client.tails.tail_dict_json.update( 
            {str(datetime.today())[:-7]: multy_pay_dict})
        client.tails.save()
    else:
        client.tails.current_tail_form_two += multy_pay_dict['tail_form_two'] 
        client.tails.active_tails_form_two += 1
        multy_pay_dict.pop('tail_form_one', None)
        client.tails.tail_dict_json_cash.update( 
            {str(datetime.today())[:-7]: multy_pay_dict})
        client.tails.save()


