from datetime import datetime
from typing import OrderedDict
from django.test import TestCase

from rest_framework import serializers
from product_eggs.models.documents import DocumentsContractEggsModel, DocumentsDealEggsModel
from product_eggs.services.balance import get_new_balance_model
from product_eggs.services.data_class.data_class_documents import PayOrderDataForSave, PayOrderDataForSaveMultiClear
from product_eggs.services.documents.docs_deleter import JsonDataDeleter
from product_eggs.services.documents.documents_get import DataNumberJsonSaver

from product_eggs.tests.create_models import TestModelCreator


DOCUMENT_TYPES = [
    'UPD_incoming', 'UPD_outgoing', 'UPD_logic', 'application_contract_logic',
    'payment_order_outcoming_logic', 'payment_order_outcoming', 'payment_order_incoming',
    'tail_payment', 'multi_pay_order',
]

CLIENT_TYPES = [
    'seller', 'buyer', 'logic',
]


class TestJsonDeleter(TestCase):

    def create_deal_users_docs(self):
        test_obj = TestModelCreator()
        self.deal = test_obj.create_base_deal(3)
        self.manager = test_obj.create_user('manager')
        self.logic = test_obj.create_user('logic')
        self.napr = test_obj.create_user('napr')
        self.fin = test_obj.create_user('fin')
        self.buh = test_obj.create_user('buh')

    def create_payorderdataforsave(self, doc_id: str, new_create: bool = True):
        if new_create and not self.deal:
            self.create_deal_users_docs()
        else:
            user: int = self.manager.pk
            date: str = str(datetime.now())[:-7]
            number: str = '120938'
            pay_quantity: float = 12930.1
            inn: str = '12093102391'
            deal: str = self.deal.pk
            doc_type: str = 'UPD_outgoing'
            entity: str = self.deal.entity.inn
            documents_id: str = doc_id
            client_type: str = 'buyer'
            force: bool = False
            self.payorderdataforsave = PayOrderDataForSave(
                user=user,
                date=date,
                number=number,
                pay_quantity=pay_quantity,
                inn=inn,
                deal=deal,
                doc_type=doc_type,
                entity=entity,
                documents_id=documents_id,
                client_type=client_type,
                force=force,
            )

    def create_payorderdataforsavemulticlear(self):
        self.create_deal_users_docs()
        user: int = self.manager.pk
        date: str = str(datetime.now())[:-7]
        number: str = '120938'
        inn: str = '12093102391'
        entity: str = self.deal.entity.inn
        total_amount: float = 12930.1
        self.payorderdataforsavemulticlear = PayOrderDataForSaveMultiClear(
            user=user,
            date=date,
            number=number,
            inn=inn,
            entity=entity,
            total_amount=total_amount,
        )

    def create_data_num_jsons(
            self,
            cur_json: PayOrderDataForSaveMultiClear | PayOrderDataForSave,
            cur_instance: DocumentsDealEggsModel | DocumentsContractEggsModel,
        ):
        obj = DataNumberJsonSaver(
            docs_nums_date=cur_json,
            instance=cur_instance,
        )
        if isinstance(cur_json, PayOrderDataForSave):
            obj.data_number_json_saver()
        if isinstance(cur_json, PayOrderDataForSaveMultiClear):
            obj.multy_pay_json_saver()

    def create_serializer_data(self, json_key: str, cash: bool = False):
        self.serializer_data = OrderedDict([('json_key', json_key), ('cash', cash), ('client_type', 'buyer')])

    def test_deal_doc_and_doc_contract(self):
        self.create_deal_users_docs()
        self.balance_model = get_new_balance_model(self.deal.entity.inn, self.deal.buyer)
        self.create_payorderdataforsave(doc_id=self.deal.buyer.documents_contract.pk, new_create=False)
        cur_doc_contract = DocumentsContractEggsModel.objects.get(pk=self.deal.buyer.documents_contract.pk)
        self.assertFalse(cur_doc_contract.data_number_json)
        self.create_data_num_jsons(self.payorderdataforsave, cur_doc_contract)
        cur_doc_contract = DocumentsContractEggsModel.objects.get(pk=self.deal.buyer.documents_contract.pk)
        self.assertTrue(cur_doc_contract.data_number_json)
        self.create_serializer_data(list(cur_doc_contract.data_number_json.keys())[0])
        del_test_obj = JsonDataDeleter(
            serializer_data=self.serializer_data,
            doc_contract_pk=cur_doc_contract.pk,
            cancel_user=self.fin,
        )
        del_test_obj.main()
        cur_doc_contract = DocumentsContractEggsModel.objects.get(pk=self.deal.buyer.documents_contract.pk)
        self.assertFalse(cur_doc_contract.data_number_json)

        # self.create_payorderdataforsavemulticlear()









