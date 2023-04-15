from typing import OrderedDict
import uuid
from django.db import transaction

from rest_framework import serializers

from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs
from product_eggs.models.tails import TailsContragentModelEggs
from users.models import CustomUser


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
            {str(uuid.uuid4()): multy_pay_dict})
        client.tails.save()
        client.save()
    else:
        client.tails.current_tail_form_two += multy_pay_dict['tail_form_two'] 
        client.tails.active_tails_form_two += 1
        multy_pay_dict.pop('tail_form_one', None)
        client.tails.tail_dict_json_cash.update( 
            {str(uuid.uuid4()): multy_pay_dict})
        client.tails.save()
        client.save()


def subtract_tail_amount_and_actives(
        instance: TailsContragentModelEggs,
        key: dict[str, str]) -> None:
    """
    Subtract dict and active.
    """
    try:
        if key['form_one']:
            instance.active_tails_form_one -= 1
            if isinstance(instance.tail_dict_json, dict):
                instance.tail_dict_json.pop(key['form_one'], None)
                instance.save()
        elif key['form_two']:
            instance.active_tails_form_two -= 1
            if isinstance(instance.tail_dict_json_cash, dict):
                instance.tail_dict_json_cash.pop(key['form_two'], None)
                instance.save()
        else:
            raise serializers.ValidationError(
                'wrong form-key in tmo_key_dict_json.')
    except KeyError as e:
        raise serializers.ValidationError(
            f'Error in subtract tail data.{e}')


@transaction.atomic
def transaction_tails_data(
        parse_val_data: dict,
        instance: TailsContragentModelEggs,
        user: CustomUser,
        key_dict: dict) -> None:
    """
    Tail data transtaction.
    """
    from product_eggs.services.documents.documents import parse_multy_payment_json

    parse_multy_payment_json(
        parse_val_data,
        user,
        current_document_contract=None,
    )
    subtract_tail_amount_and_actives(instance, key_dict)


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

