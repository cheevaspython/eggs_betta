import logging
from datetime import datetime
from django.db import transaction
from rest_framework import serializers

from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.balance import get_balance_for_tail
from product_eggs.services.data_class.data_class_documents import (
    OtherPays, PayOrderDataForSaveMultiClear, PrePayOrderDataForSave, TailTransactionData
)
from product_eggs.services.documents.documents_get import DataNumberJsonSaver
from product_eggs.services.get_anything.try_to_get_models import (
    get_client_for_tail_pk, return_client_type
)
from product_eggs.services.tails import transaction_tails_data
from product_eggs.services.data_class.data_class_documents import MultiTails
from product_eggs.services.tails import verificate_total_tail_amount_and_pay_quantity
from users.models import CustomUser

logger = logging.getLogger(__name__)


class ComparePayQuantinyAndTail():
    """
    copare other_pays pay_quantity and client json data pay_quantity
    recousia if pay_quantity > json_payquantity
    """
    def __init__(
            self,
            instance: TailsContragentModelEggs,
            user: CustomUser,
            ) -> None:
        try:
            self.multi_tails = MultiTails(**instance.multi_tails)
        except TypeError as e:
            raise serializers.ValidationError('wrong multi_tails documents in recoursia', e)
        # print(self.multi_tails.entity, type(self.multi_tails.entity))
        self.instance = instance
        verificate_total_tail_amount_and_pay_quantity(self.instance, self.multi_tails)
        self.user = user
        self.form_type = 'form_two' if self.multi_tails.cash else 'form_one'
        self.client = get_client_for_tail_pk(self.instance.pk)

    def _create_dict_for_transaction(
            self,
            uuid: str,
            tail: dict,
            pay_quantity: str,
            delta: float,
            deal_docs_pk: int) -> TailTransactionData:
        """
        Create TailTransactionData.
        """
        pre_pay_order_data = PrePayOrderDataForSave(
            date=datetime.now().date().strftime('%d/%m/%Y'),
            number=tail['number'],
            pay_quantity=pay_quantity,
            inn=self.client.inn,
            doc_type=self.multi_tails.doc_type,
            entity=self.multi_tails.entity,
            client_type=return_client_type(self.client),
            cash=self.multi_tails.cash,
            # force: bool = False
        )
        trans_data = TailTransactionData(
            tail=self.instance,
            pre_pay_data=pre_pay_order_data,
            delta=delta,
            uuid=uuid,
            user=self.user,
            doc_deal_pk=deal_docs_pk
        )
        return trans_data

    def _tail_pay_recoursia(self, cur_other_pay: OtherPays):
        tails_forms = {
            'form_one': self.instance.data_number_json,
            'form_two': self.instance.data_number_json_cash,
        }
        try:
            for uuid, tail in tails_forms[self.form_type].items():
                delta = cur_other_pay.pay_quantity - tail['pay_quantity']
                self.instance = transaction_tails_data(
                        self._create_dict_for_transaction(
                        uuid,
                        tail,
                        str(cur_other_pay.pay_quantity),
                        delta,
                        int(cur_other_pay.deal_docs_pk),
                    ),
                )
                if delta > 0:
                    cur_other_pay.pay_quantity = delta
                    return self._tail_pay_recoursia(cur_other_pay)
                else:
                    return
        except (RuntimeError, TypeError) as e:
            logging.debug('recoursia tails error, or tails == 0', e)

    def _update_data_num_json(self) -> None:
        if cur_balance := get_balance_for_tail(self.instance):
            if cur_balance.entity and self.client.documents_contract:
                save_data = PayOrderDataForSaveMultiClear(
                    user=self.user.pk,
                    date=datetime.now().date().strftime('%d/%m/%Y'),
                    number=self.multi_tails.doc_type,
                    inn=self.client.inn,
                    entity=str(cur_balance.entity.inn),
                    total_amount=self.multi_tails.total_pay,
                )
                saver_obj = DataNumberJsonSaver(
                    save_data,
                    self.client.documents_contract,
                )
                saver_obj.multy_pay_json_saver()
        else:
            logging.debug('recoursia tails error, update json')

    @transaction.atomic
    def main(self):
        for cur_other_pay in self.multi_tails.other_pays:
            self._tail_pay_recoursia(cur_other_pay)
        self._update_data_num_json()
        self.instance.multi_tails = {}
        self.instance.save()


