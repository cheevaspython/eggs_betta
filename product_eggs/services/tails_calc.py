from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.decorators import try_decorator_param


@try_decorator_param(('KeyError',), return_value=0)
def calc_client_tail_debt(tail: TailsContragentModelEggs):
    return tail.current_tail_form_one + tail.current_tail_form_two
