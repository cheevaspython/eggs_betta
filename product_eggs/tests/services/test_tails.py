from dataclasses import asdict

from django.test import TestCase

from rest_framework import serializers
from product_eggs.models.balance import BalanceBaseClientEggs

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.tails import TailsContragentModelEggs
# from product_eggs.services.data_class.data_class import TailTransactionData
from product_eggs.services.data_class.data_class_documents import (
    MultiTails, OtherPays, PayOrderDataForSaveMulti, PrePayOrderDataForSave, TailTransactionData
)
from product_eggs.services.documents.documents_parse_tmp_json import DealDocumentsPaymentParser
from product_eggs.services.get_anything.try_to_get_models import get_client_for_inn
from product_eggs.services.tails.tails import (
    subtract_tail_edit_amount_and_actives,
    TailsTreatment, transaction_tails_data, verificate_total_tail_amount_and_pay_quantity
)
from product_eggs.services.tails.tails_recoursia import ComparePayQuantinyAndTail
from product_eggs.tests.create_models import TestModelCreator
from users.models import CustomUser


class TestTailsService(TestCase):

    def create_pay_data(
            self,
            client_type: str = 'seller',
            doc_type: str = 'payment_order_outcoming',
            cash: bool | None = None,
            entity: str = '5612163931',
            pay_quantity: str = '1000000') -> dict:
        pay_data = {
            'date': '09/09/2023',
            'number': '102',
            'inn': '1234567890',
            'cash': cash,
            'entity': entity,
            'pay_quantity': pay_quantity,
            'doc_type': doc_type,
            'client_type': client_type,
        }
        return pay_data

    def create_test_object(
            self,
            deal_status: int = 3,
            client_type: str = 'seller',
            doc_type: str = 'payment_order_outcoming',
            cash: bool | None = None,
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
        if self.deal.documents:
            self.pay_data['inn'] = self.deal.seller.inn
            self.parse_data = DealDocumentsPaymentParser(
                PrePayOrderDataForSave(**self.pay_data),
                self.user,
                self.deal.documents,
            )

    def create_dict_transaction(self,
            client_type: str = 'seller',
            tail_one: float | None = None,
            tail_two: float | None = None,
            doc_type: str | None = None,
            cash: bool = False,
            delta: float | None = None,
            many_otherpays: bool = False) -> TailTransactionData:
        self.create_payorderdataforsave(client_type=client_type, tail_one=tail_one, tail_two=tail_two)
        client = None
        if not doc_type:
            doc_type = 'payment_order_outcoming'
        if delta == None:
            delta = 5000

        match client_type:
            case 'seller':
                client = self.deal.seller
            case 'buyer':
                client = self.deal.buyer
                if cash:
                    self.deal.cash = True
            case 'logic':
                client = self.deal.current_logic
        other_pays = None
        if client and delta:
            if many_otherpays:
                other_pays_list = []
                dict_other_pays = []
                for i in range(5):
                    tmp =  self.create_other_pays_object(
                        pay_quantity='5000' + str(i)
                    )
                    other_pays_list.append(tmp)
                    dict_other_pays.append(asdict(tmp))
                other_pays = other_pays_list
                if self.balance.tails:
                    self.balance.tails.multi_tails = {
                        'other_pays': dict_other_pays,
                        'doc_type': 'tail_payment',
                    }
                    self.balance.tails.save()
            else:
                if self.deal.documents and self.balance.tails:
                    other_pays = self.create_other_pays_object(
                    docs_id=self.deal.documents.pk,
                    pay_quantity='50000')

                    self.balance.tails.multi_tails = {
                        'other_pays': [asdict(other_pays)],
                        'doc_type': 'tail_payment',
                    }

            TailsTreatment(self.data_payorder, client).add_dict_json()
            self.cur_client = get_client_for_inn(
                    client.inn,
                    client_type
            )
            if self.cur_client and self.balance.tails and other_pays:
                if cash:
                    form_type = 'form_two'
                    self.assertTrue(self.balance.tails.data_number_json_cash)
                    self.uuid = list(self.balance.tails.data_number_json_cash.keys())[0]
                    self.deal.cash = True
                else:
                    form_type = 'form_one'
                    self.assertTrue(self.balance.tails.data_number_json)
                    self.uuid = list(self.balance.tails.data_number_json.keys())[0]
            else:
                self.fail('client wrong')


            self.comp_obj = ComparePayQuantinyAndTail(
                self.balance.tails,
                self.user,
            )
            tail_dict = self.balance.tails.data_number_json.values()[0]
            result = self.comp_obj._create_dict_for_transaction(
                uuid=self.uuid,
                tail=tail_dict,
                pay_quantity=other_pays[0].pay_quantity,
                delta=delta,
                deal_docs_pk=other_pays[0].deal_docs_pk,
            )
            return result
        raise KeyError('client_type')

    def test_verificate_total_tail_amount_and_pay_quantity(self):
        tail_amount = 100000
        self.create_payorderdataforsave(tail_one=tail_amount)
        client = self.deal.seller
        TailsTreatment(self.data_payorder, client).add_dict_json()
        if self.deal.documents:
            other_pays_1 = self.create_other_pays_object(
                pay_quantity='80000',
                docs_id=self.deal.documents.pk,
            )
            other_pays_2 = self.create_other_pays_object(
                pay_quantity='1000',
                docs_id=self.deal.documents.pk,
            )
            other_pays_3 = self.create_other_pays_object(
                pay_quantity='20000',
                docs_id=self.deal.documents.pk,
            )

            tail = TailsContragentModelEggs.objects.get(pk=self.deal.seller.cur_balance.all()[0].tails.pk)
            tail.multi_tails = {
                'other_pays': [asdict(other_pays_1), asdict(other_pays_2), asdict(other_pays_3)],
                'cash': False,
                'entity': '5612163931',
                'doc_type': 'tail_payment',
            }
            res = MultiTails(**tail.multi_tails)
            self.assertRaises(serializers.ValidationError, verificate_total_tail_amount_and_pay_quantity, tail, res)

            tail_amount = 100000
            self.create_payorderdataforsave(tail_one=tail_amount)
            client = self.deal.seller
            TailsTreatment(self.data_payorder, client).add_dict_json()
            other_pays_1 = self.create_other_pays_object(
                pay_quantity='70000',
                docs_id=self.deal.documents.pk,
            )
            other_pays_2 = self.create_other_pays_object(
                pay_quantity='1000',
                docs_id=self.deal.documents.pk,
            )
            other_pays_3 = self.create_other_pays_object(
                pay_quantity='20000',
                docs_id=self.deal.documents.pk,
            )
            tail = TailsContragentModelEggs.objects.get(pk=self.deal.seller.cur_balance.all()[0].tails.pk)
            tail.multi_tails = {
                'other_pays': [asdict(other_pays_1), asdict(other_pays_2), asdict(other_pays_3)],
                'cash': False,
                'entity': '5612163931',
                'doc_type': 'tail_payment',
            }
            res = MultiTails(**tail.multi_tails)
            # self.assertRaises(
            #     serializers.ValidationError,
            #     verificate_total_tail_amount_and_pay_quantity,
            #     tail,
            #     res)

    def test_tail_pay_recoursia_eq(self):
        tail_amount = 100000
        self.create_payorderdataforsave(client_type='seller',tail_one=tail_amount)
        client = self.deal.seller
        if self.balance.tails and self.deal.documents:
            tail = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
            tail2 = TailsContragentModelEggs.objects.get(pk=self.deal.seller.cur_balance.all()[0].tails.pk)
            self.assertEqual(tail, tail2)
            TailsTreatment(self.data_payorder, client).add_dict_json()
            self.balance = BalanceBaseClientEggs.objects.get(pk=self.balance.pk)

            other_pays_1 = self.create_other_pays_object(
                pay_quantity='70000',
                docs_id=self.deal.documents.pk,
            )
            other_pays_2 = self.create_other_pays_object(
                pay_quantity='1000',
                docs_id=self.deal.documents.pk,
            )
            other_pays_3 = self.create_other_pays_object(
                pay_quantity='2000',
                docs_id=self.deal.documents.pk,
            )
            if self.balance.tails:
                tail = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
            tail.multi_tails = {
                'other_pays': [asdict(other_pays_1), asdict(other_pays_2), asdict(other_pays_3)],
                'entity': '5612163931',
                'cash': False,
                'doc_type': 'tail_payment',
            }
            res = MultiTails(**tail.multi_tails)
            tail.multi_tails = asdict(res)
            old = tail.current_tail_form_one
            self.assertFalse(self.deal.deal_our_pay_amount)
            self.assertTrue(old)
            self.assertEqual(old, tail_amount)
            self.assertTrue(tail.multi_tails)
            user = self.deal.owner
            if user:
                ComparePayQuantinyAndTail(tail, user).main()
                new_res = TailsContragentModelEggs.objects.get(pk=tail.pk)
                res_pay = 70000 + 1000 + 2000
                self.assertEqual(old - res_pay, new_res.current_tail_form_one)
                res_deal = BaseDealEggsModel.objects.get(pk=self.deal.pk)
                self.assertEqual(res_deal.deal_our_pay_amount, res_pay)

    def test_tail_pay_recoursia_max_2(self):
        tail_amount = 200
        self.create_payorderdataforsave(client_type='seller',tail_one=tail_amount)
        client = self.deal.seller
        if self.balance.tails and self.deal.documents:
            tail = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
            # tail.current_tail_form_one = 100
            TailsTreatment(self.data_payorder, client).add_dict_json()
            self.balance = BalanceBaseClientEggs.objects.get(pk=self.balance.pk)
            if self.balance.tails:
                tail = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)

            other_pays_1 = self.create_other_pays_object(
                pay_quantity='120',
                docs_id=self.deal.documents.pk,
            )
            other_pays_2 = self.create_other_pays_object(
                pay_quantity='30',
                docs_id=self.deal.documents.pk,
            )
            other_pays_3 = self.create_other_pays_object(
                pay_quantity='25',
                docs_id=self.deal.documents.pk,
            )
            tail.multi_tails = {
                'other_pays': [asdict(other_pays_1), asdict(other_pays_2), asdict(other_pays_3)],
                'cash': False,
                'entity': '5612163931',
                'doc_type': 'tail_payment',
            }
            res = MultiTails(**tail.multi_tails)
            tail.multi_tails = asdict(res)
            old = tail.current_tail_form_one
            self.assertFalse(self.deal.deal_our_pay_amount)
            self.assertTrue(old)
            # self.assertEqual(old, tail_amount*2)
            self.assertTrue(tail.multi_tails)
            user = self.deal.owner
            if user:
                ComparePayQuantinyAndTail(tail, user).main()
                new_res = TailsContragentModelEggs.objects.get(pk=tail.pk)
                res_pay = 120 + 30 + 25
                self.assertEqual(old - res_pay, new_res.current_tail_form_one)
                res_deal = BaseDealEggsModel.objects.get(pk=self.deal.pk)
                self.assertEqual(res_deal.deal_our_pay_amount, res_pay)

    def create_other_pays_object(
            self,
            docs_id: int | None = None,
            pay_quantity: str = '1000000',
            ) -> OtherPays:
        if not docs_id and self.deal.documents:
            docs_id = self.deal.documents.pk
        if docs_id:
            otherpays_object = OtherPays(
                deal_docs_pk=str(docs_id),
                pay_quantity=pay_quantity,
            )
            return otherpays_object
        raise ValueError('docs_id in tests wrong')

    def test_creator_otherpays_obj(self):
        self.create_test_object()
        otherpays_object = self.create_other_pays_object()
        self.assertIs(type(otherpays_object), OtherPays)
        self.assertIs(type(otherpays_object.pay_quantity), float)

    def create_payorderdataforsave(
            self,
            client_type: str = 'seller',
            tail_one: float | None = None,
            tail_two: float | None = None,
            doc_type: str = 'tail_payment',
            many_otherpays: bool = False,
            ):
        self.test_obj = TestModelCreator()
        self.deal = self.test_obj.create_base_deal(3)
        self.bal_type_book = {
            'seller': self.deal.seller,
            'buyer': self.deal.buyer,
            'logic': self.deal.current_logic,
        }
        self.balance = self.test_obj.create_balance(self.bal_type_book[client_type])
        self.user: CustomUser = self.test_obj.create_user('manager')
        self.date: str = '09.09.2023'
        number: str = '12938'
        self.total_amount: str = '100000'
        inn: str = self.test_obj.create_random_inn()
        if many_otherpays:
            other_pays = []
            for i in range(5):
                other_pays.append(
                    self.create_other_pays_object(pay_quantity='5000' + str(i)))
        else:
            if self.deal.documents:
                other_pays = asdict(self.create_other_pays_object(
                    docs_id=self.deal.documents.pk,
                    pay_quantity='50000'))
            else:
                raise serializers.ValidationError()
        client_type=client_type
        tail_form_one = tail_one
        tail_form_two = tail_two
        if self.deal.entity:
            self.data_payorder = PayOrderDataForSaveMulti(
                user=self.user.pk,
                date=self.date,
                number=number,
                total_amount=float(self.total_amount),
                inn=inn,
                entity=self.deal.entity.inn,
                other_pays=other_pays,
                client_type=client_type,
                tail_form_one=tail_form_one,
                tail_form_two=tail_form_two,
            )

    def test_tails_treatment_seller(self):
        tail_amount = 100000
        self.create_payorderdataforsave(tail_one=tail_amount)
        client = self.deal.seller
        tail = TailsContragentModelEggs.objects.get(pk=self.deal.seller.cur_balance.all()[0].tails.pk)
        tail.current_tail_form_one = 0
        tail.current_tail_form_two = 0
        tail.active_tails_form_one = 0
        tail.active_tails_form_two = 0
        if self.balance.tails:
            self.assertFalse(self.balance.tails.data_number_json)
            TailsTreatment(self.data_payorder, client).add_dict_json()
            self.balance = BalanceBaseClientEggs.objects.get(pk=self.balance.pk)

            if self.balance.tails:
                new = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
                self.assertEqual(tail.pk, new.pk)
                self.assertEqual(self.balance.tails.current_tail_form_one, tail_amount)
                self.assertEqual(self.balance.tails.active_tails_form_one, 1)
                self.assertFalse(self.balance.tails.active_tails_form_two)
                self.assertFalse(self.balance.tails.current_tail_form_two)
                self.assertTrue(self.balance.tails.data_number_json)

        self.create_payorderdataforsave(tail_two=tail_amount)
        client = self.deal.seller
        tail = TailsContragentModelEggs.objects.get(pk=self.deal.seller.cur_balance.all()[0].tails.pk)
        tail.current_tail_form_one = 0
        tail.current_tail_form_two = 0
        tail.active_tails_form_one = 0
        tail.active_tails_form_two = 0
        if self.balance.tails:
            self.assertFalse(self.balance.tails.data_number_json)
            TailsTreatment(self.data_payorder, client).add_dict_json()
            self.balance = BalanceBaseClientEggs.objects.get(pk=self.balance.pk)
        if self.balance.tails:
            self.assertEqual(self.balance.tails.current_tail_form_two, tail_amount)
            self.assertEqual(self.balance.tails.active_tails_form_two, 1)
            self.assertFalse(self.balance.tails.active_tails_form_one)
            self.assertFalse(self.balance.tails.current_tail_form_one)
            self.assertTrue(self.balance.tails.data_number_json_cash)

    def test_tails_treatment_buyer(self):
        tail_amount = 100000
        self.create_payorderdataforsave(client_type='buyer', tail_one=tail_amount)
        client = self.deal.buyer
        tail = TailsContragentModelEggs.objects.get(pk=self.deal.buyer.cur_balance.all()[0].tails.pk)
        tail.current_tail_form_one = 0
        tail.current_tail_form_two = 0
        tail.active_tails_form_one = 0
        tail.active_tails_form_two = 0
        if self.balance.tails:
            self.assertFalse(self.balance.tails.data_number_json)
        TailsTreatment(self.data_payorder, client).add_dict_json()
        if self.balance.tails:
            self.balance = BalanceBaseClientEggs.objects.get(pk=self.balance.pk)
        if self.balance.tails:
            self.assertEqual(self.balance.tails.current_tail_form_one, tail_amount)
            self.assertEqual(self.balance.tails.active_tails_form_one, 1)
            self.assertFalse(self.balance.tails.active_tails_form_two)
            self.assertFalse(self.balance.tails.current_tail_form_two)
            self.assertTrue(self.balance.tails.data_number_json)

        self.create_payorderdataforsave(client_type='buyer', tail_two=tail_amount)
        client = self.deal.buyer
        tail = TailsContragentModelEggs.objects.get(pk=self.deal.buyer.cur_balance.all()[0].tails.pk)
        tail.current_tail_form_one = 0
        tail.current_tail_form_two = 0
        tail.active_tails_form_one = 0
        tail.active_tails_form_two = 0
        if self.balance.tails:
            self.assertFalse(self.balance.tails.data_number_json)
        TailsTreatment(self.data_payorder, client).add_dict_json()
        if self.balance.tails:
            self.balance = BalanceBaseClientEggs.objects.get(pk=self.balance.pk)
        if self.balance.tails:
            self.assertEqual(self.balance.tails.current_tail_form_two, tail_amount)
            self.assertEqual(self.balance.tails.active_tails_form_two, 1)
            self.assertFalse(self.balance.tails.active_tails_form_one)
            self.assertFalse(self.balance.tails.current_tail_form_one)
            self.assertTrue(self.balance.tails.data_number_json_cash)

    def test_tails_treatment_logic(self):
        tail_amount = 100000
        self.create_payorderdataforsave(client_type='logic', tail_one=tail_amount)
        client = self.deal.current_logic
        tail = TailsContragentModelEggs.objects.get(pk=self.deal.current_logic.cur_balance.all()[0].tails.pk)
        tail.current_tail_form_one = 0
        tail.current_tail_form_two = 0
        tail.active_tails_form_one = 0
        tail.active_tails_form_two = 0
        if self.balance.tails:
            self.assertFalse(self.balance.tails.data_number_json)
        if client:
            TailsTreatment(self.data_payorder, client).add_dict_json()
        if self.balance.tails:
            self.balance = BalanceBaseClientEggs.objects.get(pk=self.balance.pk)
        if self.balance.tails:
            self.assertEqual(self.balance.tails.current_tail_form_one, tail_amount)
            self.assertEqual(self.balance.tails.active_tails_form_one, 1)
            self.assertFalse(self.balance.tails.active_tails_form_two)
            self.assertFalse(self.balance.tails.current_tail_form_two)
            self.assertTrue(self.balance.tails.data_number_json)

        self.create_payorderdataforsave(client_type='logic', tail_two=tail_amount)
        client = self.deal.current_logic
        tail = TailsContragentModelEggs.objects.get(pk=self.deal.current_logic.cur_balance.all()[0].tails.pk)
        tail.current_tail_form_one = 0
        tail.current_tail_form_two = 0
        tail.active_tails_form_one = 0
        tail.active_tails_form_two = 0
        if self.balance.tails:
            self.assertFalse(self.balance.tails.data_number_json)
        if client:
            TailsTreatment(self.data_payorder, client).add_dict_json()
        if self.balance.tails:
            self.balance = BalanceBaseClientEggs.objects.get(pk=self.balance.pk)
        if self.balance.tails:
            self.assertEqual(self.balance.tails.current_tail_form_two, tail_amount)
            self.assertEqual(self.balance.tails.active_tails_form_two, 1)
            self.assertFalse(self.balance.tails.active_tails_form_one)
            self.assertFalse(self.balance.tails.current_tail_form_one)
            self.assertTrue(self.balance.tails.data_number_json_cash)

    def test_tails_treatment_wrong(self):
        tail_amount = 100000
        self.create_payorderdataforsave(client_type='buyer', tail_one=tail_amount)
        client = self.deal.seller
        self.assertRaises(serializers.ValidationError, TailsTreatment, self.data_payorder, client)

        self.create_payorderdataforsave(client_type='seller', tail_two=tail_amount)
        client = self.deal.current_logic
        self.assertRaises(serializers.ValidationError, TailsTreatment, self.data_payorder, client)

        # self.create_payorderdataforsave(client_type='superman', tail_two=tail_amount)
        # client = self.deal.current_logic
        # self.assertRaises(serializers.ValidationError, TailsTreatment, self.data_payorder, client)

        self.create_payorderdataforsave(client_type='seller', tail_two=tail_amount)
        client = self.deal.documents
        self.assertRaises(serializers.ValidationError, TailsTreatment, self.data_payorder, client)

    def test_create_dict_for_transaction(self):
        tail_amount = 100000
        self.create_payorderdataforsave(tail_two=tail_amount)
        client = self.deal.seller
        self.assertTrue(self.deal.seller.cur_balance)
        tail = TailsContragentModelEggs.objects.get(pk=self.deal.seller.cur_balance.last().tails.pk)
        tail.current_tail_form_one = 0
        tail.current_tail_form_two = 0
        tail.active_tails_form_one = 0
        tail.active_tails_form_two = 0
        if self.balance.tails:
            self.assertFalse(self.balance.tails.data_number_json)
        TailsTreatment(self.data_payorder, client).add_dict_json()
        self.balance = BalanceBaseClientEggs.objects.get(pk=self.balance.pk)
        if self.balance.tails:
            self.assertEqual(self.balance.tails.current_tail_form_two, tail_amount)
            self.assertEqual(self.balance.tails.active_tails_form_two, 1)
            self.uuid = list(self.balance.tails.data_number_json_cash.keys())[0]
        self.assertTrue(self.uuid)
        if self.deal.documents:
            other_pays = self.create_other_pays_object(
                docs_id=self.deal.documents.pk,
                pay_quantity='50000')
        # res_obj = ComparePayQuantinyAndTail(
        #
        # )
        # result = res_obj._create_dict_for_transaction(
        #     self.uuid,
        #     delta=1000,
        # )
        # self.assertIs(type(result), TailTransactionData)
        # self.assertTrue(result.date)

    # def test_transaction_tails_data(self):
    #     tail_amount = 100000
    #     self.create_test_object()
    #     transaction_data = self.create_dict_transaction(
    #         client_type='logic',
    #         tail_two=tail_amount,
    #         cash=True,
    #         doc_type='payment_order_outcoming_logic',
    #     )
    #     user = self.deal.owner
    #     cur_tail = self.deal.current_logic.cur_balance.tails
    #     self.deal.delivery_form_payment = 3
    #     self.deal.save()
    #     uuid = list(cur_tail.data_number_json_cash.keys())[0]
    #     delta = 222000
    #     self.assertIs(type(transaction_data.pre_pay_data), PrePayOrderDataForSave)
    #     self.assertEqual(transaction_data.uuid, uuid)
    #     self.assertEqual(transaction_data.user, user)
    #     self.assertEqual(transaction_data.delta, delta)
    #     self.assertEqual(transaction_data.doc_deal_pk, self.deal.documents.pk)




