import logging

from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.data_class.data_class import TailTransactionData
from product_eggs.services.data_class.data_class_documents import \
    OtherPays
from product_eggs.services.tails import transaction_tails_data
from users.models import CustomUser
                
logger = logging.getLogger(__name__)
                 

def create_dict_for_transaction(
        instance: TailsContragentModelEggs,
        ulid,
        cur_pay: OtherPays,
        form_one: float | None = None,
        form_two: float | None = None) -> TailTransactionData:

    trans_data = TailTransactionData(
        date = None,
        number = instance.tail_dict_json[ulid]['number'],
        inn = instance.tail_dict_json[ulid]['inn'],
        total_amount = 0, 
        tail_form_one = form_one,
        tail_form_two = form_two,
        other_pays = cur_pay,
    ) 
    return trans_data 


def tail_pay_recoursia(
        instance_pk: int,
        cur_pay: OtherPays,
        user: CustomUser,
        form_type: str) -> None:
    """
    Tail multi pay for one click.
    entry -> Otherpays, where deals and pay_quantity,
    plus current tailmodel.
    Pay whis deals, cur tails.
    """
    instance = TailsContragentModelEggs.objects.get(pk=instance_pk)

    tails_forms = {
        'form_one': (instance.tail_dict_json, 'tail_form_one', False), 
        'form_two': (instance.tail_dict_json_cash, 'tail_form_two', True), 
    }

    if cur_pay.pay_quantity:
        try:
            for ulid, tail in tails_forms[form_type][0].items(): 
                if cur_pay.pay_quantity > tail[tails_forms[form_type][1]]:
                    new_cur_pay = OtherPays(**cur_pay.__dict__)
                    new_cur_pay.pay_quantity -= tail[tails_forms[form_type][1]]
                    cur_pay.pay_quantity = tail[tails_forms[form_type][1]]
                    transaction_tails_data(
                        create_dict_for_transaction(
                            instance,
                            ulid,
                            cur_pay,
                        ),
                        user,
                        instance,
                        ulid,
                        cash=tails_forms[form_type][2]
                    )
                    return tail_pay_recoursia(instance.pk, new_cur_pay, user, form_type)

                elif cur_pay.pay_quantity < tail[tails_forms[form_type][1]]:
                    new_cur_pay = OtherPays(**cur_pay.__dict__)
                    new_cur_pay.pay_quantity = 0
                    transaction_tails_data(
                        create_dict_for_transaction(
                            instance,
                            ulid,
                            cur_pay,
                        ),
                        user,
                        instance,
                        ulid,
                        delta=float(cur_pay.pay_quantity),
                        mini_sub=True,
                        cash=tails_forms[form_type][2]
                    )
                    return tail_pay_recoursia(instance.pk, new_cur_pay, user, form_type)
                else:
                    new_cur_pay = OtherPays(**cur_pay.__dict__)
                    new_cur_pay.pay_quantity = 0
                    transaction_tails_data(
                        create_dict_for_transaction(
                            instance,
                            ulid,
                            cur_pay,
                        ),
                        user,
                        instance,
                        ulid,
                        cash=tails_forms[form_type][2]
                    )
                    return 
        except RuntimeError as e:
            logging.debug('recoursia tails error', e)
    else:
        pass
