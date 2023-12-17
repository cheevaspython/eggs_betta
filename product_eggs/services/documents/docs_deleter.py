import logging
from collections import namedtuple
from typing import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.base_deal.deal_messages_payment import data_num_json_canceled_send_message
from product_eggs.services.documents.documents_srv import subtract_deal_pays_then_del_datanum
from product_eggs.models.documents import DocumentsContractEggsModel
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.data_class.data_class import DeleteJson, TailDataForJsonSave
from product_eggs.services.data_class.data_class_documents import (
    PayOrderDataForSave, PayOrderDataForSaveMultiClear
)
from product_eggs.services.get_anything.try_to_get_models import get_client_for_doc_contract
from product_eggs.services.validationerror import custom_error
from users.models import CustomUser

logger = logging.getLogger(__name__)


class JsonDataDeleter():
    """
    1. get 2 istances
    2. trancaction for:
       calc balance after del and subs
       del 2 jsons (in two instances)
    3. get data_num, parse
    4. sub deal
    5. tails
    6. del json
    7. commit transaction
    8. cancel message to fin
    """
    DictjsonAndCurDataclass = namedtuple('json_dataclass', ['path_json', 'cur_dataclass'])
    DeleteJsonBook = namedtuple('json_for_delete', ['doc_json_type', 'cur_json'])
    doc_multi_parse_book: DeleteJsonBook | None = None
    doc_contract_parse_book: DeleteJsonBook | None = None
    doc_contract_cash_parse_book: DeleteJsonBook | None = None
    doc_deal_book: DeleteJsonBook | None = None
    doc_deal_cash_book: DeleteJsonBook | None = None
    doc_tail_book: DeleteJsonBook | None = None
    doc_tail_cash_book: DeleteJsonBook | None = None
    deal = None
    deal_id = None
    tail = None

    def __init__(self,
            serializer_data: OrderedDict,
            doc_contract_pk: str,
            cancel_user: CustomUser) -> None:

        self.delete_data = DeleteJson(**serializer_data)
        self.doc_contract_pk = doc_contract_pk
        self.cancel_user = cancel_user
        self._finded_jsons = list()

    def _get_doc_contract_model(self):
        try:
            doc_pk = int(self.doc_contract_pk)
        except ValueError as e:
            raise custom_error(f'wrong pk data, cant convert to integer {e}', 433)
        try:
            self.cur_doc_cont: DocumentsContractEggsModel  = DocumentsContractEggsModel.objects.get(pk=doc_pk)
            self.client: SellerCardEggs | BuyerCardEggs | LogicCardEggs = \
                get_client_for_doc_contract(self.cur_doc_cont, self.delete_data.client_type)
        except (KeyError, AttributeError, ObjectDoesNotExist) as e:
            logging.debug('delete json error, wrong doc type or client', e)
            raise custom_error('cant get doc_contract or client for delete', 433)

    def construct_contract_models_book(self) -> dict:
        """
        create books model
        cantract for default,
        deal and tail -> if true
        """
        doc_contract_json_book = {
            'doc_multi': self.DictjsonAndCurDataclass(self.cur_doc_cont.multy_pay_json, PayOrderDataForSaveMultiClear,),
            'doc_contract': self.DictjsonAndCurDataclass(self.cur_doc_cont.data_number_json, PayOrderDataForSave,),
            'doc_contract_cash': self.DictjsonAndCurDataclass(self.cur_doc_cont.data_number_json_cash, PayOrderDataForSave,),
        }
        if isinstance(self.tail, TailsContragentModelEggs):
            doc_contract_json_book['doc_tail'] = self.DictjsonAndCurDataclass(self.tail.data_number_json, TailDataForJsonSave,)
            doc_contract_json_book['doc_tail_cash'] = self.DictjsonAndCurDataclass(self.tail.data_number_json_cash, TailDataForJsonSave,)
        if isinstance(self.deal, BaseDealEggsModel) and self.deal.documents:
            doc_contract_json_book['doc_deal'] = self.DictjsonAndCurDataclass(self.deal.documents.data_number_json, PayOrderDataForSave,)
            doc_contract_json_book['doc_deal_cash'] = self.DictjsonAndCurDataclass(self.deal.documents.data_number_json_cash, PayOrderDataForSave,)
        return doc_contract_json_book

    def try_get_contract_convert_json(
            self,
            doc_json_type: str
            ) -> DeleteJsonBook | None:
        """
        return json and type if exists
        """
        try:
            parse_json = self.construct_contract_models_book()[doc_json_type].cur_dataclass(
                **self.construct_contract_models_book()[doc_json_type].path_json[self.delete_data.json_key])
            return self.DeleteJsonBook(doc_json_type, parse_json)
        except (KeyError, AttributeError, ObjectDoesNotExist):
            return None

    def _get_parse_json(self) -> None:
        """
        add results (for contragent model) in _finded_jsons list
        """
        self.doc_multi_parse_book = self.try_get_contract_convert_json('doc_multi')
        self.doc_contract_parse_book = self.try_get_contract_convert_json('doc_contract')
        self.doc_contract_cash_parse_book = self.try_get_contract_convert_json('doc_contract_cash')

        self._finded_jsons.append(self.doc_multi_parse_book) if self.doc_multi_parse_book else None
        self._finded_jsons.append(self.doc_contract_parse_book) if self.doc_contract_parse_book else None
        self._finded_jsons.append(self.doc_contract_cash_parse_book) if self.doc_contract_cash_parse_book else None

    def _get_entity(self) -> None:
        if self._finded_jsons:
            self.entity_inn = self._finded_jsons[0].cur_json.entity
        else:
            raise custom_error('finded json for key -> empty. Doc contragent havent jsons with cur key', 433)

    def _get_cur_balance(self) -> None:
        try:
            self.current_balance = self.client.cur_balance.get(entity=self.entity_inn)
            self.tail = self.current_balance.tails
        except (KeyError, AttributeError, ObjectDoesNotExist):
            raise custom_error(f'cant get current balance for client {self.client}, entity {self.entity_inn}', 433)

    def _get_all_jsons(self) -> None:
        """
        add all results to _finded_jsons list
        """
        if self.doc_contract_parse_book and isinstance(self.doc_contract_parse_book.cur_json, PayOrderDataForSave):
            self.deal_id = self.doc_contract_parse_book.cur_json.deal
        elif self.doc_contract_cash_parse_book and isinstance(self.doc_contract_cash_parse_book.cur_json, PayOrderDataForSave):
            self.deal_id = self.doc_contract_cash_parse_book.cur_json.deal
        if self.deal_id:
            self.deal = BaseDealEggsModel.objects.get(pk=self.deal_id)
            if self.deal and self.deal.documents:
                self.doc_deal_book = self.try_get_contract_convert_json('doc_deal')
                self.doc_deal_cash_book = self.try_get_contract_convert_json('doc_deal_cash')
        if self.tail:
            self.doc_tail_book = self.try_get_contract_convert_json('doc_tail')
            self.doc_tail_cash_book = self.try_get_contract_convert_json('doc_tail_cash')
        self._finded_jsons.append(self.doc_deal_book) if self.doc_deal_book else None
        self._finded_jsons.append(self.doc_deal_cash_book) if self.doc_deal_cash_book else None
        self._finded_jsons.append(self.doc_tail_book) if self.doc_tail_book else None
        self._finded_jsons.append(self.doc_tail_cash_book) if self.doc_tail_cash_book else None

    def _find_books_action(self):
        """
        for any type jsons in _finded_jsons apply actions
        """
        if self._finded_jsons:
            for cur_book in self._finded_jsons:
                match cur_book.doc_json_type:
                    case 'doc_multi':
                        del self.cur_doc_cont.multy_pay_json[self.delete_data.json_key]
                        self._send_cancel_message(cur_book.cur_json)
                    case 'doc_contract':
                        del self.cur_doc_cont.data_number_json[self.delete_data.json_key]
                        self._send_cancel_message(cur_book.cur_json)
                    case 'doc_contract_cash':
                        del self.cur_doc_cont.data_number_json_cash[self.delete_data.json_key]
                        self._send_cancel_message(cur_book.cur_json)
                    case 'doc_deal':
                        subtract_deal_pays_then_del_datanum(
                            cur_book.cur_json, self.current_balance, self.delete_data.json_key
                        )
                        self._send_cancel_message(cur_book.cur_json)
                    case 'doc_deal_cash':
                        subtract_deal_pays_then_del_datanum(
                            cur_book.cur_json, self.current_balance, self.delete_data.json_key
                        )
                        self._send_cancel_message(cur_book.cur_json)
                    case 'doc_tail':
                        if self.tail:
                            update_tail = TailsContragentModelEggs.objects.get(pk=self.tail.pk)
                            update_tail.current_tail_form_one -= cur_book.cur_json['pay_quantity']
                            update_tail.active_tails_form_one -= 1
                            del update_tail.data_number_json[self.delete_data.json_key]
                            self._send_cancel_message(cur_book.cur_json)
                            update_tail.save()
                    case 'doc_tail_cash':
                        if self.tail:
                            update_tail = TailsContragentModelEggs.objects.get(pk=self.tail.pk)
                            update_tail.current_tail_form_two -= cur_book.cur_json['pay_quantity']
                            update_tail.active_tails_form_two -= 1
                            del update_tail.data_number_json_cash[self.delete_data.json_key]
                            self._send_cancel_message(cur_book.cur_json)
                    case _:
                        pass

    def _save_models(self) -> None:
        """
        save contragent model
        """
        if self.doc_multi_parse_book and self.doc_contract_parse_book:
            self.cur_doc_cont.save()
        elif self.doc_multi_parse_book and self.doc_contract_cash_parse_book:
            self.cur_doc_cont.save()
        elif self.doc_multi_parse_book:
            self.cur_doc_cont.save()
        elif self.doc_contract_parse_book:
            self.cur_doc_cont.save()
        elif self.doc_contract_cash_parse_book:
            self.cur_doc_cont.save()
        else:
            pass

    def _action_and_save(self) -> None:
        with transaction.atomic():
            self._find_books_action()
            self._save_models()

    def _send_cancel_message(
            self,
            json_data: PayOrderDataForSave | PayOrderDataForSaveMultiClear | TailDataForJsonSave) -> None:
        data_num_json_canceled_send_message(
            json_data,
            self.client,
            self.cancel_user
        )

    # @transaction.atomic
    def main(self) -> None:
        self._get_doc_contract_model()
        self._get_parse_json()
        self._get_entity()
        self._get_cur_balance()
        self._get_all_jsons()
        self._action_and_save()






