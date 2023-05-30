import logging
import uuid

from dataclasses import asdict
from typing import OrderedDict

from django.db import transaction
from rest_framework import serializers

from product_eggs.models.base_client import BuyerCardEggs, \
    LogicCardEggs, SellerCardEggs
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.data_class.data_class import TailTransactionData
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.documents.documents_parse_tmp_json import \
    MultiDocumentsPaymentParser
from users.models import CustomUser

logger = logging.getLogger(__name__)


def add_tail_model_to_client(
        client: BuyerCardEggs | SellerCardEggs | LogicCardEggs) -> None:
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
        client: BuyerCardEggs | SellerCardEggs | None = None,
        cur_tail: TailsContragentModelEggs | None = None):
    """
    add deposit in form
    add count tails
    save model
    """
    if cur_tail:
        if multy_pay_dict['tail_form_one']:
            cur_tail.current_tail_form_one += multy_pay_dict['tail_form_one'] 
            cur_tail.active_tails_form_one += 1
            multy_pay_dict.pop('tail_form_two', None)
            cur_tail.tail_dict_json.update( 
                {str(uuid.uuid4()): multy_pay_dict})
            cur_tail.multi_tails = {}
            cur_tail.save()
        elif multy_pay_dict['tail_form_two']:
            cur_tail.current_tail_form_two += multy_pay_dict['tail_form_two'] 
            cur_tail.active_tails_form_two += 1
            multy_pay_dict.pop('tail_form_one', None)
            cur_tail.tail_dict_json_cash.update( 
                {str(uuid.uuid4()): multy_pay_dict})
            cur_tail.multi_tails = {}
            cur_tail.save()
        else:
            cur_tail.save()

    elif client:
        add_tail_model_to_client(client)

        if multy_pay_dict['tail_form_one']:
            client.tails.current_tail_form_one += multy_pay_dict['tail_form_one'] 
            client.tails.active_tails_form_one += 1
            multy_pay_dict.pop('tail_form_two', None)
            client.tails.tail_dict_json.update( 
                {str(uuid.uuid4()): multy_pay_dict})
            client.tails.multi_tails = {}
            client.tails.save()
        else:
            client.tails.current_tail_form_two += multy_pay_dict['tail_form_two'] 
            client.tails.active_tails_form_two += 1
            multy_pay_dict.pop('tail_form_one', None)
            client.tails.tail_dict_json_cash.update( 
                {str(uuid.uuid4()): multy_pay_dict})
            client.tails.multi_tails = {}
            client.tails.save()


def subtract_tail_edit_amount_and_actives(
        instance: TailsContragentModelEggs,
        ulid,
        delta: float) -> TailsContragentModelEggs | None:
    "edit ulid dict, not del"

    try:
        if instance.tail_dict_json[ulid]:
            instance.current_tail_form_one -= delta
            new_form_one = instance.tail_dict_json[ulid]['tail_form_one'] - delta
            instance.tail_dict_json[ulid]['tail_form_one'] = new_form_one
            return instance
    except KeyError as e:
        logging.debug('error sub tail edit', e)
        pass

    try:
        if instance.tail_dict_json_cash[ulid]:
            instance.current_tail_form_two -= delta
            new_form_one = instance.tail_dict_json_cash[ulid]['tail_form_two'] - delta
            instance.tail_dict_json_cash[ulid]['tail_form_two'] = new_form_one
            return instance
    except KeyError as e:
        logging.debug('error sub tail edit', e)
        pass


def subtract_tail_amount_and_actives(
        instance: TailsContragentModelEggs,
        ulid,) -> TailsContragentModelEggs | None:
    """
    Subtract dict and active.
    """
    try:
        if instance.tail_dict_json[ulid]:
            instance.active_tails_form_one -= 1
            instance.current_tail_form_one -= \
                instance.tail_dict_json[ulid]['tail_form_one']
            instance.tail_dict_json.pop(ulid, None)
            return instance

    except KeyError as e:
        logging.debug('error sub tail', e)
        pass

    try:
        if instance.tail_dict_json_cash[ulid]:
            instance.active_tails_form_two -= 1
            instance.current_tail_form_two -= \
                instance.tail_dict_json[ulid]['tail_form_one']
            instance.tail_dict_json_cash.pop(ulid, None)
            return instance

    except KeyError as e:
        logging.debug('error sub tail', e)
        pass


@transaction.atomic
def transaction_tails_data(
        transaction_data: TailTransactionData,
        user: CustomUser,
        instance: TailsContragentModelEggs,
        ulid: dict,
        cash: bool = False,
        delta: float | None = None,
        mini_sub: bool = False) -> None:
    """
    Tail data transtaction.
    """
    if mini_sub and delta:
        edit_inst = subtract_tail_edit_amount_and_actives(
            instance, ulid, delta
        )
    else:
        edit_inst = subtract_tail_amount_and_actives(instance, ulid)

    parse_tail = MultiDocumentsPaymentParser(
        asdict(transaction_data),
        user,
        current_document_contract=None,
        cur_tail=edit_inst,
        cash=cash,
    )
    parse_tail.main()


def wrong_entry_tail_data(validated_data: OrderedDict) -> None:
    """
    Check val_data tails for wrong data.
    Raise error if find.
    """
    wrong_fields = [
        'current_tail_form_one', 'current_tail_form_two',
        'active_tails_form_one', 'active_tails_form_two',
        'tail_dict_json', 'tail_dict_json_cash',
    ]
    for field in validated_data.values():
        if field in wrong_fields:
            raise serializers.ValidationError(
                'Wrong entry data for pay_tails, only tmp_json')


@try_decorator_param(('KeyError',))
def check_validated_tails_data_for_fields(validated_data: OrderedDict) -> bool:
    if validated_data['tmp_json_for_multi_pay_order'] and \
            validated_data['tmp_key_form_dict']:
        return True
    else: 
        return False
