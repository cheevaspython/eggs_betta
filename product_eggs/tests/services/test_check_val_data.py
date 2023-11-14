from dataclasses import asdict
from datetime import datetime
from django.test import TestCase
from collections import OrderedDict
from general_layout.documents.models.docs_for_contragent import DocumentsContragentModel

from product_eggs.models.base_client import SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsContractEggsModel, DocumentsDealEggsModel
from product_eggs.models.messages import MessageToUserEggs
from product_eggs.services.data_class.data_class_documents import PayOrderDataForSave
from product_eggs.services.validation.check_validated_data import (
    check_data_for_note, check_val_data_contract_multy_pay,
    check_validated_data_for_tmp_json
)
from product_eggs.tests.create_models import TestModelCreator


class TestCheckValData(TestCase):

    def create_pay_data(self,
        entity: str = '5612163931',
        ) -> dict:

        pay_data = {
            'date': '09/09/2023',
            'number': '102',
            'inn': '1234567890',
            'cash': False,
            'entity': entity,
            'pay_quantity': '1000000',
            'doc_type': 'UPD_incoming',
            'client_type': 'seller',
        }
        return pay_data

    def create_test_object(self, deal_status: int):
        self.test_obj = TestModelCreator()
        self.user = self.test_obj.create_user('manager')
        self.pay_data = self.create_pay_data()
        self.deal = self.test_obj.create_base_deal(deal_status)
        self.pay_data['inn'] = self.deal.seller.inn

    def test_check_data_for_note(self):
        test_obj = TestModelCreator()
        deal = test_obj.create_base_deal(3)
        user = test_obj.create_user('manager')
        test_data = OrderedDict([('one', 'two'), ('note_calc', 'test_note')])
        self.assertTrue(check_data_for_note(test_data, deal, 'note_calc', user))
        test_data_2 = OrderedDict([('one', 'two'), ('foo', 'test_note')])
        self.assertFalse(check_data_for_note(test_data_2, deal, 'note_calc', user))
        mess = MessageToUserEggs.objects.get(pk=1)
        self.assertEqual(mess.message_to, deal.owner)
        self.assertEqual(mess.current_base_deal, deal)

    def test_check_validated_data_for_tmp_json(self):
        test_obj = TestModelCreator()
        today_dt = str(datetime.today())[:-6]
        user = test_obj.create_user('manager')
        self.create_test_object(3)
        test_data = OrderedDict([('one', 'two'), ('foo', 'test_note'), ('tmp_json', self.pay_data)])
        if self.deal.documents:
            check_validated_data_for_tmp_json(test_data, self.deal.documents, user)
            self.pay_data['user'] = user.pk
            self.pay_data['deal'] = self.deal.pk
            self.pay_data['documents_id'] = self.deal.documents.pk
            self.pay_data['pay_quantity'] = float(self.pay_data['pay_quantity'])
            del self.pay_data['cash']
            result = PayOrderDataForSave(**self.pay_data)
            self.assertTrue(self.deal.documents.data_number_json)
            # print(self.deal.documents.data_number_json.items(), '\n', asdict(result))
            # self.assertTrue(asdict(result) in self.deal.documents.data_number_json.items())
            #
            # update_seller = SellerCardEggs.objects.get(pk=self.deal.seller.pk)
            # self.assertTrue(asdict(result) in update_seller.documents_contract.data_number_json.items())
        else:
            self.fail()

    def test_check_val_data_contract_multy_pay(self):
        ...#TODO
# check_val_data_contract_multy_pay()
#
#         serializer_data: OrderedDict,
#         instance: DocumentsContractEggsModel,
#         user: CustomUser) -> bool:
#
#     if check_data_for_value(serializer_data, 'multi_pay_order') and \
#             check_data_for_value(serializer_data, 'tmp_json_multi_pay_order'):
#         multi_data = convert_front_data_to_prepaydataforsavemulti(serializer_data)
#         instance.multi_pay_order_links_dict_json.update(
#             {str(datetime.today())[:-7]: (DOC_CONTRACT_MULTY_PAY +
#                 str(serializer_data['multi_pay_order']))}
#         )
#         parse_multi = MultiDocumentsPaymentParser(
#             multi_data,
#             user,
#             instance,
#         )
#         parse_multi.main()
#         return True
#
#     elif check_data_for_value(serializer_data, 'tmp_json_multi_pay_order'):
#         if serializer_data['tmp_json_multi_pay_order']['cash']:
#             multi_data = convert_front_data_to_prepaydataforsavemulti(serializer_data)
#             if check_data_for_value(serializer_data, 'multi_pay_order_cash'):
#                 instance.multi_pay_order_cash_links.update(
#                     {str(datetime.today())[:-7]: (DOC_CONTRACT_CASH +
#                         str(serializer_data['multi_pay_order_cash']))}
#                 )
#             parse_multi = MultiDocumentsPaymentParser(
#                 multi_data,
#                 user,
#                 instance,
#             )
#             parse_multi.main()
#             return True
#
#         else:
#             raise serializers.ValidationError(
#                 'wrong tmp_json_multi_pay_order data (tmp_json form1, but not multi_pay_order)')
#     else:
#         return False


    # def test_data_num_json_deleter(self):
    #     # self.create_test_object(3)
    #     test_obj = TestModelCreator()
    #     user = test_obj.create_user('manager')
    #     self.create_test_object(3)
    #     test_data = OrderedDict([('one', 'two'), ('foo', 'test_note'), ('tmp_json', self.pay_data)])
    #
    #     if self.deal.documents:
    #         check_validated_data_for_tmp_json(test_data, self.deal.documents, user)
    #         self.pay_data['user'] = user.pk
    #         self.pay_data['deal'] = self.deal.pk
    #         self.pay_data['documents_id'] = self.deal.documents.pk
    #         self.pay_data['pay_quantity'] = float(self.pay_data['pay_quantity'])
    #         del self.pay_data['cash']
    #         d1 = BaseDealEggsModel.objects.get(pk=self.deal.pk)
    #         self.assertTrue(d1.deal_our_pay_amount)
    #         result = PayOrderDataForSave(**self.pay_data)
    #         self.assertTrue(self.deal.documents.data_number_json)
    #         cash = False
    #         client_type = 'seller'
    #         updated_doc = DocumentsContractEggsModel.objects.get(pk=self.deal.seller.documents_contract.pk)
    #         json_key = list(updated_doc.data_number_json.keys())[0]
    #         test_del_data = OrderedDict([('json_key', json_key), ('cash', cash), ('client_type', client_type)])
    #         d2 = BaseDealEggsModel.objects.get(pk=self.deal.pk)
    #
    #         self.assertFalse(d2.deal_our_pay_amount)
    #         updated_deal_docs = DocumentsDealEggsModel.objects.get(pk=self.deal.documents.pk)
    #         updated_doc = DocumentsContractEggsModel.objects.get(pk=self.deal.seller.documents_contract.pk)
    #         self.assertFalse(updated_deal_docs.data_number_json)
    #         self.assertFalse(updated_doc.data_number_json)


         # test dlya byuer logic tail multi + pp TODO





