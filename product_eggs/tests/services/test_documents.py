from datetime import datetime, date

from dataclasses import asdict

from django.test import TestCase

from rest_framework import serializers

from product_eggs.models.base_client import SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsContractEggsModel, DocumentsDealEggsModel
from product_eggs.models.entity import EntityEggs
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.balance import get_new_balance_model
from product_eggs.services.base_deal.deal_pay_service import DealPayOrderUPDservice
from product_eggs.services.data_class.data_class_documents import (
    OtherPays, PayOrderDataForSave, PayOrderDataForSaveMulti,
    PrePayOrderDataForSave, PrePayOrderDataForSaveMulti
)
from product_eggs.services.documents.docs_get_link import DownloadDocumentsLink
from product_eggs.services.documents.documents_get import DataNumberJsonSaver
from product_eggs.services.documents.documents_parse_tmp_json import (
    DealDocumentsPaymentParser, MultiDocumentsPaymentParser
)
from product_eggs.tests.create_models import TestModelCreator


class TestDownloadDocumentsLink(TestCase):
    """
    need upload doc to test
    """

    # def test_get_link(self):
    #     test_obj = TestModelCreator()
    #     deal = test_obj.create_base_deal(3)
    #     pk_data = f'{deal.documents.pk}-specification_seller'
    #     result = DownloadDocumentsLink(pk_data)
    #     self.assertEqual(result.title, 'specification_seller')
    #     self.assertEqual(result.pk, deal.documents.pk)
    #     self.assertEqual(result._get_file_link(), str(deal.documents.specification_seller))
    #     self.assertEqual(result._get_doc_deal_instance(), deal.documents)
    #     # result.get_auto_download_response()  #TODO
    #     # self.assertTrue(result.get_auto_download_response())
    #
    #     pk_data = f'{deal.seller.documents_contract.pk}-contract'
    #     result = DownloadDocumentsLink(pk_data)
    #     self.assertEqual(result.title, 'contract')
    #     self.assertEqual(result.pk, deal.seller.documents_contract.pk)
    #     self.assertEqual(result._get_doc_contract_instance(), deal.seller.documents_contract)
    #     self.assertTrue(result.get_auto_download_response())
    #     result.get_auto_download_response()  #TODO
    #
    #     wrong_pk = '1231234-specification_seller'
    #     result = DownloadDocumentsLink(wrong_pk)
    #     self.assertEqual(result.title, 'specification_seller')
    #     self.assertRaises(serializers.ValidationError, result._get_doc_deal_instance)
    #
    #     wrong_pk = f'{deal.documents.pk}-specification_sellerOS'
    #     result = DownloadDocumentsLink(wrong_pk)
    #     self.assertNotEqual(result.title, 'specification_seller')
    #     self.assertRaises(serializers.ValidationError, result._get_file_link)
    #     self.assertRaises(serializers.ValidationError, result.get_auto_download_response)
    #
    #     wrong_pk = 'mama->specication_seller_kal'
    #     result = DownloadDocumentsLink(wrong_pk)
    #     self.assertRaises(serializers.ValidationError, result._get_doc_deal_instance)
    #     self.assertRaises(serializers.ValidationError, result.get_auto_download_response)


class TestMultyDocumentsPayParser(TestCase):

    def create_multi_pay_data(
            self,
            client_type: str = 'seller',
            total_amount: str = '1000000',
            many_otherpays: bool = False,
            doc_type: str = 'payment_order_outcoming',
            docs_id: int | None = None,
            cash: bool | None = False,
            entity: str = '5612163931',
            inn: str = TestModelCreator().create_random_inn(),
            tail_form_one: str | None = None,
            tail_form_two: str | None = None,
            ) -> PrePayOrderDataForSaveMulti:

        if not docs_id:
            docs_id = TestModelCreator().create_deal_docs().pk

        if many_otherpays:
            self.other_pays = []
            for i in range(5):
                self.other_pays.append(
                    self.create_other_pays_object(
                        pay_quantity='5000' + str(i), doc_type='payment_order_outcoming', docs_id=docs_id,
                    )
                )
        else:
            self.other_pays = self.create_other_pays_object(
            docs_id=docs_id,
            doc_type=doc_type,
            pay_quantity='50000')

        multi_pay_data = {
            'date': '09/09/2023',
            'number': '102',
            'inn': inn,
            'cash': cash,
            'entity': entity,
            'doc_type': doc_type,
            'total_amount': total_amount,
            'tail_form_one': tail_form_one,
            'tail_form_two': tail_form_two,
            'other_pays': self.other_pays,
            'client_type': client_type,
        }
        return PrePayOrderDataForSaveMulti(**multi_pay_data)

    def test_create_multi_pay_data(self):
        test_obj = TestModelCreator()
        cur_deal = test_obj.create_base_deal(3)
        result = self.create_multi_pay_data(
            client_type='seller',
            total_amount='123000',
            many_otherpays=True,
            inn=cur_deal.seller.inn,
            docs_id=cur_deal.documents.pk
        )
        self.assertEqual(result.entity, '5612163931')
        self.assertIs(type(result.other_pays), list)
        self.assertEqual(len(result.other_pays), 5)
        for i in result.other_pays:
            self.assertEqual(int(i.deal_docs_pk), cur_deal.documents.pk)

    def create_test_object(
            self,
            client_type: str = 'seller',
            total_amount: str = '1000000',
            many_otherpays: bool = False,
            deal_status: int = 1,
            tail_form_one: str | None = None,
            tail_form_two: str | None = None,
            ) -> None:
        self.test_obj = TestModelCreator()
        self.user = self.test_obj.create_user('manager')
        self.deal = self.test_obj.create_base_deal(deal_status)
        # get_new_balance_model('5612163931', self.deal.seller)
        self.pay_data = self.create_multi_pay_data(
            client_type,
            total_amount,
            many_otherpays=many_otherpays,
            inn=self.deal.seller.inn,
            docs_id=self.deal.documents.pk,
            tail_form_one=tail_form_one,
            tail_form_two=tail_form_two,
        )
        self.parse_data = MultiDocumentsPaymentParser(
            self.pay_data,
            self.user,
            self.deal.seller.documents_contract,
        )

    def create_other_pays_object(
            self,
            docs_id: int | None = None,
            pay_quantity: str = '1000000',
            doc_type: str = 'UPD_incoming',
            ) -> OtherPays:
        if not docs_id:
            docs_id = TestModelCreator().create_deal_docs().pk
        if docs_id:
            otherpays_object = OtherPays(
                deal_docs_pk=str(docs_id),
                pay_quantity=pay_quantity,
            )
            return otherpays_object
        raise ValueError('docs_id in tests wrong')

    def test_create_test_object(self):
        self.create_test_object(
            client_type='buyer',
            total_amount='123',
            many_otherpays=False,
            deal_status=2,
        )
        self.assertIs(type(self.pay_data), PrePayOrderDataForSaveMulti)
        self.assertIs(type(self.parse_data), MultiDocumentsPaymentParser)
        self.parse_data._convert_pay_multi_data()
        self.assertEqual(self.parse_data.pay_order_multi.other_pays[0].deal_docs_pk, str(self.deal.documents.pk))
        for i in self.parse_data.pay_order_multi.other_pays:
            self.assertEqual(i.deal_docs_pk, str(self.deal.documents.pk))

    def test_creator_otherpays_obj(self):
        otherpays_object = self.create_other_pays_object()
        self.assertIs(type(otherpays_object), OtherPays)
        self.assertIs(type(otherpays_object.pay_quantity), float)

    def test_multi_pay_dataclass(self):
        test_obj = TestModelCreator()
        user = test_obj.create_user('fin')
        asdict_data: dict = asdict(self.create_multi_pay_data())
        asdict_data['user'] = user.pk
        self.assertIs(type(asdict_data['doc_type']), str)
        del asdict_data['cash']
        del asdict_data['doc_type']
        pay_multi_dataclass = PayOrderDataForSaveMulti(**asdict_data)
        self.assertIs(type(pay_multi_dataclass), PayOrderDataForSaveMulti)
        self.assertIs(type(pay_multi_dataclass.total_amount), float)
        self.assertEqual(pay_multi_dataclass.user, user.pk)
        #TODO add all fields

    def test_multi_payment_parser_init(self):
        test_obj = TestModelCreator()
        multi_pay_data = asdict(self.create_multi_pay_data())
        user = test_obj.create_user('manager')
        seller = test_obj.create_seller()
        multi_pay_data['inn'] = seller.inn
        multi_parse = MultiDocumentsPaymentParser(
            PrePayOrderDataForSaveMulti(**multi_pay_data),
            user,
            seller.documents_contract,
        )
        self.assertIs(type(multi_parse), MultiDocumentsPaymentParser)
        self.assertEqual(multi_parse.user, user)
        multi_parse._convert_pay_multi_data()
        self.assertIs(type(multi_parse.pay_order_multi), PayOrderDataForSaveMulti)
        self.assertEqual(multi_parse._check_entry_data(), True)
        multi_parse._check_entry_data()
        self.assertEqual(multi_parse.client, seller)
        multi_parse.doc_contract = None
        multi_parse._get_documents_contract()
        self.assertEqual(multi_parse.doc_contract, seller.documents_contract)

    def test_check_entry_data(self):
        self.create_test_object()
        self.parse_data._convert_pay_multi_data()
        self.parse_data._check_entry_data()
        self.assertTrue(self.parse_data._check_entry_data())
        self.assertEqual(self.parse_data.client, self.deal.seller)

        self.parse_data.pay_order_multi.inn = '0000000001'
        self.assertRaises(serializers.ValidationError, self.parse_data._check_entry_data)

    def test_get_documents_contract(self):
        self.create_test_object()
        self.parse_data.doc_contract = None
        self.parse_data._convert_pay_multi_data()
        self.parse_data._check_entry_data()
        self.parse_data._get_documents_contract()
        self.assertEqual(self.parse_data.doc_contract, self.deal.seller.documents_contract)

        self.parse_data.client = None
        self.assertRaises(serializers.ValidationError, self.parse_data._get_documents_contract)

    def test_construct_other_pay(self):
        self.create_test_object(deal_status=3)
        self.parse_data._convert_pay_multi_data()
        self.parse_data._check_entry_data()
        self.parse_data._get_documents_contract()
        otherpays_object = self.create_other_pays_object(self.deal.documents)
        result = self.parse_data._construct_other_pay(otherpays_object)
        self.assertTrue(result)
        self.assertIs(type(result), PrePayOrderDataForSave)
        self.assertEqual(result.date, self.pay_data.date)
        self.assertEqual(result.number, self.pay_data.number)
        self.assertEqual(result.client_type, self.pay_data.client_type)

    def test_get_deal_docs_model(self):
        self.create_test_object(deal_status=3)
        if isinstance(self.other_pays, OtherPays):
            result = self.parse_data._get_deal_docs_model(self.other_pays.deal_docs_pk)
            self.assertIs(type(result), DocumentsDealEggsModel)
            self.assertEqual(result, self.deal.documents)

        self.create_test_object(deal_status=3, many_otherpays=True)
        if isinstance(self.other_pays, list):
            for pay in self.other_pays:
                if isinstance(self.other_pays, OtherPays):
                    result = self.parse_data._get_deal_docs_model(pay.deal_docs_pk)
                    self.assertIs(type(result), DocumentsDealEggsModel)
                    self.assertEqual(result, self.deal.documents)

    def test_send_message_to_finance_manager(self):
        self.create_test_object(deal_status=3)
        self.parse_data._convert_pay_multi_data()
        self.parse_data._check_entry_data()
        self.assertTrue(self.parse_data.client)
        self.parse_data._send_message_to_finance_manager()
        # self.assertTrue(MessageToUserEggs.objects.all())
        #TODO

    def test_splitter_multi_order(self):
        self.create_test_object(deal_status=3, many_otherpays=True)
        old_deal_data = self.deal.deal_our_pay_amount
        self.assertIs(type(self.pay_data.other_pays), list)
        sum_pay = 0
        for i in self.pay_data.other_pays:
            self.assertEqual(int(i.deal_docs_pk), self.deal.documents.pk)
            sum_pay += i.pay_quantity

        self.parse_data._convert_pay_multi_data()
        self.parse_data._check_entry_data()
        self.parse_data._get_documents_contract()
        self.parse_data._splitter_multi_order()
        result = BaseDealEggsModel.objects.get(pk=self.deal.pk)
        self.assertTrue(result.deal_our_pay_amount)
        self.assertNotEqual(result.deal_our_pay_amount, old_deal_data)
        self.assertEqual(result.deal_our_pay_amount, sum_pay)
        # mess_res = MessageToUserEggs.objects.all()
        # self.assertTrue(mess_res)
        #TODO

    def test_tail_save(self):
        tail_amount = '222000'
        self.create_test_object(deal_status=3, many_otherpays=True, tail_form_one=tail_amount)
        self.parse_data._convert_pay_multi_data()
        self.parse_data._check_entry_data()
        self.parse_data._get_documents_contract()
        self.parse_data._splitter_multi_order()
        self.parse_data._tail_save()
        cur_seller = SellerCardEggs.objects.get(inn=self.deal.seller.inn)
        self.assertEqual(cur_seller.cur_balance.all()[0].tails.current_tail_form_one, int(tail_amount))
        self.assertEqual(cur_seller.cur_balance.all()[0].tails.active_tails_form_one, 1)

    def test_multi_pay_main(self):
        test_obj = TestModelCreator()
        pay = "99999"
        multi_pay_data = asdict(self.create_multi_pay_data(
            cash=False,
            client_type="buyer",
            entity='5612163931',
            total_amount=pay,
            tail_form_one=pay,
            tail_form_two=None,
            doc_type="multi_pay_order",
        ))
        multi_pay_data['other_pays'] = []
        user = test_obj.create_user('manager')
        buyer = test_obj.create_buyer()
        multi_pay_data['inn'] = buyer.inn
        multi_parse = MultiDocumentsPaymentParser(
            PrePayOrderDataForSaveMulti(**multi_pay_data),
            user,
            buyer.documents_contract,
        )
        multi_parse.main()
        tail = buyer.cur_balance.last().tails
        self.assertEqual(tail.current_tail_form_one, float(pay))
        if buyer.documents_contract:
          res_doc = DocumentsContractEggsModel.objects.get(pk=buyer.documents_contract.pk)
          self.assertTrue(res_doc.multy_pay_json)
        else:
            self.fail()

    def test_update_data_num_doc_model_json(self):
        tail_amount = '222000'
        self.create_test_object(deal_status=3, many_otherpays=True, tail_form_one=tail_amount)
        self.parse_data._convert_pay_multi_data()
        self.parse_data._check_entry_data()
        self.parse_data._get_documents_contract()
        self.parse_data._splitter_multi_order()
        self.parse_data._tail_save()
        self.assertTrue(self.parse_data.doc_contract)
        self.assertEqual(self.parse_data.client, self.deal.seller)
        self.parse_data._update_data_num_doc_model_json()
        if self.parse_data.doc_contract:
            self.assertTrue(self.parse_data.doc_contract.multy_pay_json)
        else:
            self.fail()
        update_seller = SellerCardEggs.objects.get(pk=self.deal.seller.pk)
        self.assertTrue(update_seller.documents_contract.multy_pay_json)


class TestDocumentsPayParser(TestCase):

    def create_pay_data(
            self,
            client_type: str = 'seller',
            doc_type: str = 'UPD_incoming',
            cash: bool | None = False,
            entity: str = '5612163931',
            pay_quantity: str = '1000000') -> dict:
        pay_data = {
            'date': '09/09/2023',
            'number': '102',
            'inn': '1234567890',
            'cash': cash,
            'pay_quantity': pay_quantity,
            'doc_type': doc_type,
            'client_type': client_type,
            'entity': entity,
        }
        return pay_data

    def create_test_object(
            self,
            deal_status: int,
            client_type: str = 'seller',
            doc_type: str = 'UPD_incoming',
            cash: bool | None = False,
            pay_quantity: str = '1000000',
            ) -> None:
        self.test_obj = TestModelCreator()
        self.user = self.test_obj.create_user('manager')
        self.pay_data = self.create_pay_data(
            client_type=client_type,
            doc_type=doc_type,
            cash=cash,
            pay_quantity=pay_quantity
        )
        self.deal = self.test_obj.create_base_deal(deal_status)
        self.pay_data['inn'] = self.deal.seller.inn
        self.parse_data = DealDocumentsPaymentParser(
            PrePayOrderDataForSave(**self.pay_data),
            self.user,
            self.deal.documents,
        )

    def test_docs_parser_init(self):
        self.create_test_object(3)
        self.assertEqual(self.parse_data.client_documents_model, self.deal.seller.documents_contract)
        self.assertIs(type(self.parse_data.pay_data), dict)
        self.assertEqual(self.parse_data.user, self.user)
        self.assertEqual(self.parse_data.instance, self.deal.documents)
        self.assertEqual(self.parse_data.deal, self.deal)

    def test_check_entry_data(self):
        self.create_test_object(4)
        self.parse_data._check_entry_data()
        self.assertEqual(self.parse_data.client_documents_model, self.deal.seller.documents_contract)

    def test_update_pay_data_and_convert(self):
        self.create_test_object(3)
        self.parse_data._update_pay_data()
        self.assertEqual(self.parse_data.pay_data['user'], self.user.pk)
        self.assertEqual(self.parse_data.pay_data['deal'], self.deal.pk)
        self.assertEqual(self.parse_data.pay_data['documents_id'], self.deal.documents.pk)
        self.parse_data._convert_pay_data()
        self.assertIs(type(self.parse_data.converted_pay_data), PayOrderDataForSave)

        self.create_test_object(3, pay_quantity='mama mila ramu')
        self.assertRaises(serializers.ValidationError, self.parse_data._update_pay_data)

    def test_update_and_save_data_number_json(self):
        self.create_test_object(3)
        self.parse_data._update_pay_data()
        self.parse_data._convert_pay_data()
        self.assertEqual(self.parse_data.client_documents_model, self.deal.seller.documents_contract)

        saver = DataNumberJsonSaver(
            self.parse_data.converted_pay_data,
            self.parse_data.instance,
        )
        saver.data_number_json_saver()

        self.assertEqual(self.parse_data.instance.data_number_json[saver.general_uuid], asdict(self.parse_data.converted_pay_data))
        self.parse_data._check_entry_data()

    def test_update_and_save_data_number_json2(self):
        self.create_test_object(3)
        self.parse_data._update_pay_data()
        self.parse_data._convert_pay_data()
        self.assertEqual(self.parse_data.client_documents_model, self.deal.seller.documents_contract)
        saver = DataNumberJsonSaver(
            self.parse_data.converted_pay_data,
            self.deal.seller.documents_contract,
        )
        saver.data_number_json_saver()

        cur_doc = DocumentsContractEggsModel.objects.get(pk=self.parse_data.client_documents_model.pk)
        self.assertTrue(cur_doc.data_number_json)
        self.assertEqual(cur_doc.data_number_json[saver.general_uuid], asdict(self.parse_data.converted_pay_data))
        self.assertEqual(self.parse_data.client_documents_model, self.deal.seller.documents_contract)
        update_seller = SellerCardEggs.objects.get(pk=self.deal.seller.pk)
        self.assertEqual(update_seller.documents_contract.data_number_json[saver.general_uuid], asdict(self.parse_data.converted_pay_data))

    def test_update_and_save_data_number_json3(self):
        self.create_test_object(3)
        self.parse_data._update_pay_data()
        self.parse_data._convert_pay_data()
        self.assertEqual(self.parse_data.client_documents_model, self.deal.seller.documents_contract)
        saver = DataNumberJsonSaver(
            self.parse_data.converted_pay_data,
            self.deal.seller.documents_contract,
        )
        saver.data_number_json_saver()
        saver.multy_pay_json_saver()

        cur_doc = DocumentsContractEggsModel.objects.get(pk=self.parse_data.client_documents_model.pk)
        self.assertTrue(cur_doc.data_number_json)
        self.assertEqual(cur_doc.multy_pay_json[saver.general_uuid], asdict(self.parse_data.converted_pay_data))
        self.assertEqual(cur_doc, self.deal.seller.documents_contract)
        update_seller = SellerCardEggs.objects.get(pk=self.deal.seller.pk)
        self.assertEqual(update_seller.documents_contract.multy_pay_json[saver.general_uuid], asdict(self.parse_data.converted_pay_data))
        self.assertTrue(update_seller.documents_contract.multy_pay_json)

    def test_update_and_save_data_number_json4(self):
        self.create_test_object(3)
        self.parse_data._update_pay_data()
        self.parse_data._convert_pay_data()
        self.assertEqual(self.parse_data.client_documents_model, self.deal.seller.documents_contract)
        saver = DataNumberJsonSaver(
            self.parse_data.converted_pay_data,
            self.parse_data.client_documents_model
        )
        saver.data_number_json_saver()

        cur_doc = DocumentsContractEggsModel.objects.get(pk=self.parse_data.client_documents_model.pk)
        self.assertTrue(cur_doc.data_number_json)
        self.assertEqual(cur_doc.data_number_json[saver.general_uuid], asdict(self.parse_data.converted_pay_data))

        self.parse_data._update_model_field()
        self.assertEqual(self.parse_data.client_documents_model.data_number_json[saver.general_uuid], asdict(self.parse_data.converted_pay_data))
        update_seller = SellerCardEggs.objects.get(pk=self.deal.seller.pk)
        self.assertEqual(update_seller.documents_contract.data_number_json[saver.general_uuid], asdict(self.parse_data.converted_pay_data))

    def test_deal_service_create_and_action(self):
        self.create_test_object(3)
        self.parse_data._update_pay_data()
        self.assertEqual(self.parse_data.pay_data['user'], self.user.pk)
        self.assertEqual(self.parse_data.pay_data['deal'], self.deal.pk)
        if self.deal.documents:
            self.assertEqual(self.parse_data.pay_data['documents_id'], self.deal.documents.pk)
            self.parse_data._convert_pay_data()
            self.assertIs(type(self.parse_data.converted_pay_data), PayOrderDataForSave)
            self.assertFalse(self.deal.payback_day_for_us)
            self.parse_data._deal_service_create_action()
            self.parse_data.deal_service_object.deal.save()
            self.assertTrue(self.parse_data.deal_service_object)
            self.assertIs(type(self.parse_data.deal_service_object), DealPayOrderUPDservice)
            self.assertTrue(self.parse_data.deal_service_object)
            self.assertIs(type(self.parse_data.deal_service_object.deal.payback_day_for_us), date)
            cur_deal = BaseDealEggsModel.objects.get(pk=self.deal.pk)
            self.assertIs(type(cur_deal.payback_day_for_us), date)
        else:
            self.fail()

    def test_main(self):
        self.create_test_object(3)
        result = self.deal.deal_our_pay_amount
        self.parse_data.main_default()
        deal = BaseDealEggsModel.objects.get(pk=self.deal.pk)
        self.assertNotEqual(deal.deal_our_pay_amount, result)
        self.assertTrue(deal.payback_day_for_us)




