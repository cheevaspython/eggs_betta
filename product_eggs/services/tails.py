from datetime import datetime
import uuid

from dataclasses import asdict

from typing import OrderedDict

from django.db import transaction

from rest_framework import serializers
from product_eggs.models.balance import BalanceBaseClientEggs

from product_eggs.models.base_client import (
    BuyerCardEggs, LogicCardEggs, SellerCardEggs
)
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.balance import get_cur_balance
from product_eggs.services.data_class.data_class import (
    TailDataForJsonSave
)
from product_eggs.services.data_class.data_class_documents import (
    MultiTails, PayOrderDataForSave, PayOrderDataForSaveMulti, TailTransactionData
)
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.documents.documents_parse_tmp_json import (
    DealDocumentsPaymentParser,
)
from product_eggs.services.get_anything.try_to_get_models import (
    check_client_type_and_model
)


def create_tail_model_to_balance() -> TailsContragentModelEggs:
    """
    if balance dont have related tail
    create new tail model and save
    """
    new_tail = TailsContragentModelEggs.objects.create()
    new_tail.save()
    return new_tail


class TailsTreatment():
    """
    Add tail amount to cur tails client + add json.
    """
    def __init__(
            self,
            multi_pay: PayOrderDataForSaveMulti,
            client: BuyerCardEggs | SellerCardEggs | LogicCardEggs,
            general_uuid: str | None = None):
        check_client_type_and_model(client, multi_pay.client_type)
        self.client = client
        self.tail_form_one = multi_pay.tail_form_one
        self.tail_form_two = multi_pay.tail_form_two
        self.user = multi_pay.user
        self.date = multi_pay.date
        self.number = multi_pay.number
        self.entity = multi_pay.entity
        if general_uuid:
            self.general_uuid = general_uuid
        else:
            self.general_uuid = str(datetime.today())[:-7] + ' , ' + str(uuid.uuid4())

    def create_data_for_tails_dict(self) -> TailDataForJsonSave:
        save_data = TailDataForJsonSave(
            user=self.user,
            date=self.date,
            number=self.number,
            pay_quantity=self.pay_quantity,
            entity=self.entity
        )
        return save_data

    def add_dict_json(self):
        cur_balance = get_cur_balance(self.entity, self.client)

        if not cur_balance.tails:
            cur_balance.tails = create_tail_model_to_balance()
            cur_balance.save()

        if self.tail_form_one:
            cur_tail = cur_balance.tails
            self.pay_quantity = float(self.tail_form_one)
            cur_tail.current_tail_form_one += self.pay_quantity
            cur_tail.active_tails_form_one += 1
            cur_tail.data_number_json.update(
                {self.general_uuid: asdict(self.create_data_for_tails_dict())})
            cur_tail.multi_tails = {}
            cur_tail.save()

        elif self.tail_form_two:
            cur_tail = cur_balance.tails
            self.pay_quantity = float(self.tail_form_two)
            cur_tail.current_tail_form_two += self.pay_quantity
            cur_tail.active_tails_form_two += 1
            cur_tail.data_number_json_cash.update(
                {self.general_uuid: asdict(self.create_data_for_tails_dict())})
            cur_tail.multi_tails = {}
            cur_tail.save()

        else:
            pass


def subtract_tail_edit_amount_and_actives(transaction_data: TailTransactionData) -> TailTransactionData:
    """
    """
    if transaction_data.delta >= 0:
        if transaction_data.pre_pay_data.cash:
            transaction_data.tail.current_tail_form_two -= \
                transaction_data.tail.data_number_json_cash[transaction_data.uuid]['pay_quantity']
            transaction_data.tail.active_tails_form_two -= 1
            if transaction_data.delta:
                transaction_data.pre_pay_data.pay_quantity = \
                    transaction_data.tail.data_number_json_cash[transaction_data.uuid]['pay_quantity']
            del transaction_data.tail.data_number_json_cash[transaction_data.uuid]
            return transaction_data
        else:
            transaction_data.tail.current_tail_form_one -= \
                transaction_data.tail.data_number_json[transaction_data.uuid]['pay_quantity']
            transaction_data.tail.active_tails_form_one -= 1
            if transaction_data.delta:
                transaction_data.pre_pay_data.pay_quantity = \
                    transaction_data.tail.data_number_json[transaction_data.uuid]['pay_quantity']
            del transaction_data.tail.data_number_json[transaction_data.uuid]
            return transaction_data
    else:
        if transaction_data.pre_pay_data.cash:
            transaction_data.tail.current_tail_form_two -= float(transaction_data.pre_pay_data.pay_quantity)
            transaction_data.tail.data_number_json_cash[transaction_data.uuid]['pay_quantity'] = abs(transaction_data.delta)
            return transaction_data
        else:
            transaction_data.tail.current_tail_form_one -= float(transaction_data.pre_pay_data.pay_quantity)
            transaction_data.tail.data_number_json[transaction_data.uuid]['pay_quantity'] = abs(transaction_data.delta)
            return transaction_data


@transaction.atomic
def transaction_tails_data(transaction_data: TailTransactionData) -> TailsContragentModelEggs:
    """
    Tail data transtaction.
    """
    edit_data = subtract_tail_edit_amount_and_actives(transaction_data)
    parse_tail = DealDocumentsPaymentParser(
        edit_data.pre_pay_data,
        edit_data.user,
        DocumentsDealEggsModel.objects.get(pk=edit_data.doc_deal_pk),
    )
    parse_tail.main_default()
    return transaction_data.tail


@try_decorator_param(('KeyError',))
def check_validated_tails_data_for_fields(validated_data: OrderedDict) -> bool:
    if validated_data['tmp_json_for_multi_pay_order'] and \
            validated_data['tmp_key_form_dict']:
        return True
    else:
        return False


def verificate_total_tail_amount_and_pay_quantity(
        instance: TailsContragentModelEggs, multitails: MultiTails) -> None:
    try:
        if multitails.cash:
            if multitails.total_pay > instance.current_tail_form_two:
                raise serializers.ValidationError('pay_quantity sum in OtherPays > tail sum client cash')
        else:
            if multitails.total_pay > instance.current_tail_form_one:
                raise serializers.ValidationError('pay_quantity sum in OtherPays > tail sum client')
    except KeyError as e:
        raise serializers.ValidationError('wrong tail instance', e)


def tail_return_to_balance_and_del_old(
        data_num_json: PayOrderDataForSave,
        cur_balance: BalanceBaseClientEggs,
        cash: bool) -> None:

    save_data = TailDataForJsonSave(
        user=data_num_json.user,
        date=data_num_json.date,
        number=data_num_json.number,
        pay_quantity=data_num_json.pay_quantity,
        entity=data_num_json.entity,
    )
    general_uuid = str(datetime.today())[:-7] + ' , ' + str(uuid.uuid4())

    if cur_tail := cur_balance.tails:
        if cash:
            cur_tail.current_tail_form_two += data_num_json.pay_quantity
            cur_tail.active_tails_form_two += 1
            # del cur_tail.data_number_json_cash[json_key]
            cur_tail.data_number_json_cash.update(
                {general_uuid: asdict(save_data)})
            cur_tail.multi_tails = {}
            cur_tail.save()
        else:
            cur_tail = cur_balance.tails
            cur_tail.current_tail_form_one += data_num_json.pay_quantity
            cur_tail.active_tails_form_one += 1
            # del cur_tail.data_number_json_cash[json_key]
            cur_tail.data_number_json.update(
                {general_uuid: asdict(save_data)})
            cur_tail.multi_tails = {}
            cur_tail.save()






