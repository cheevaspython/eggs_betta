from datetime import datetime, timedelta

from rest_framework import serializers

from django.db.models.query import QuerySet
from django.test import TestCase

from product_eggs.models.messages import MessageToUserEggs
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.base_deal.deal_messages_payment import delta_UPD_send_message
from product_eggs.services.base_deal.deal_pay_compare import compare_UPD_and_payments
from product_eggs.services.base_deal.deal_pay_service import DealPayOrderUPDservice
from product_eggs.services.data_class.data_class_documents import PayOrderDataForSave
from product_eggs.tests.create_models import TestModelCreator


class TestPayOrderUPDService(TestCase):

    def create_pay_data(
            self,
            client_type: str = 'seller',
            doc_type: str = 'UPD_incoming',
            pay_quantity: str = '1000000') -> dict:
        pay_data = {
            'number': '102',
            'pay_quantity': pay_quantity,
            'doc_type': doc_type,
            'client_type': client_type,
        }
        return pay_data

    def create_payorder_dataclass(
            self,
            client_type: str = 'seller',
            doc_type: str = 'UPD_incoming',
            pay_quantity: str = '1000000',
            entity: str = '5612163931',
            force_bool: bool = False,) -> PayOrderDataForSave:
        self.test_obj = TestModelCreator()
        self.deal = self.test_obj.create_base_deal(3)
        self.bal_type_book = {
            'seller': self.deal.seller,
            'buyer': self.deal.buyer,
            'logic': self.deal.current_logic,
        }
        self.balance = self.test_obj.create_balance(self.bal_type_book[client_type])
        self.deal_our_debt_UPD = self.deal.deal_our_debt_UPD
        self.user = self.test_obj.create_user('manager')
        self.date_datetime = datetime.now().date()
        date = self.date_datetime.strftime("%d/%m/%Y")
        pay_data = self.create_pay_data(client_type, doc_type, pay_quantity)
        pay_dataclass = PayOrderDataForSave(
            user = self.user.pk,
            date = date,
            number = pay_data['number'],
            pay_quantity = float(pay_data['pay_quantity']),
            inn = self.deal.seller.inn,
            entity = entity,
            documents_id = str(self.deal.documents.pk),
            deal = str(self.deal.pk),
            doc_type = pay_data['doc_type'],
            client_type = pay_data['client_type'],
            force = force_bool,
        )
        return pay_dataclass

    def test_create_payorder_dataclass(self):
        self.test_obj = TestModelCreator()
        self.deal = self.test_obj.create_base_deal(3)
        self.deal_our_debt_UPD = self.deal.deal_our_debt_UPD
        self.user = self.test_obj.create_user('manager')
        self.date_datetime = datetime.now().date()
        date = self.date_datetime.strftime("%d/%m/%Y")
        pay_data = self.create_pay_data()

        def create_wrong_client_type() -> PayOrderDataForSave:
            return PayOrderDataForSave(
                user = self.user.pk,
                date = date,
                number = pay_data['number'],
                pay_quantity = float(pay_data['pay_quantity']),
                inn = self.deal.seller.inn,
                entity = '5612163931',
                documents_id = str(self.deal.documents.pk),
                deal = str(self.deal.pk),
                doc_type = pay_data['doc_type'],
                client_type = 'some thing',
                force = False,
            )
        self.assertRaises(serializers.ValidationError, create_wrong_client_type)

        def create_wrong_doc_type() -> PayOrderDataForSave:
            return PayOrderDataForSave(
                user = self.user.pk,
                date = date,
                number = pay_data['number'],
                pay_quantity = float(pay_data['pay_quantity']),
                inn = self.deal.seller.inn,
                entity = '5612163931',
                documents_id = str(self.deal.documents.pk),
                deal = str(self.deal.pk),
                doc_type = 'some thing',
                client_type = pay_data['client_type'],
                force = False,
            )
        self.assertRaises(serializers.ValidationError, create_wrong_doc_type)

    def create_pay_order_obj(self) -> DealPayOrderUPDservice:
        self.pay_order_dataclass = self.create_payorder_dataclass()
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = self.pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.seller,
        )
        return pay_order_obj

    def get_message(self) -> QuerySet:
        return MessageToUserEggs.objects.filter(current_base_deal=self.deal)

    def test_pay_order_service_init(self):
        pay_order_obj = self.create_pay_order_obj()
        self.assertEqual(pay_order_obj.deal, self.deal)
        self.assertEqual(pay_order_obj.pay_client, self.deal.seller)
        self.assertEqual(pay_order_obj.data, self.pay_order_dataclass)

    def test_try_to_create_payback_date_if_UPD_update(self):
        pay_order_obj = self.create_pay_order_obj()
        pay_order_obj.try_to_create_payback_date_if_UPD_update()
        self.assertEqual(pay_order_obj.deal.payback_day_for_us, self.date_datetime)

    def test_add_payback_day_for_us(self):
        pay_order_obj = self.create_pay_order_obj()
        pay_order_obj.add_payback_day_for_us(self.pay_order_dataclass.date)
        self.assertEqual(pay_order_obj.deal.payback_day_for_us, self.date_datetime)

    def test_add_payback_day_for_us_1day(self):
        pay_order_obj = self.create_pay_order_obj()
        pay_order_obj.deal.postponement_pay_for_us = 1
        pay_order_obj.add_payback_day_for_us(self.pay_order_dataclass.date)
        date_plus_one_day = self.date_datetime + timedelta(days=self.deal.postponement_pay_for_us)
        self.assertEqual(pay_order_obj.deal.payback_day_for_us, date_plus_one_day)

    def test_add_payback_day_for_buyer(self):
        pay_order_obj = self.create_pay_order_obj()
        pay_order_obj.add_payback_day_for_buyer(self.pay_order_dataclass.date)
        self.assertEqual(pay_order_obj.deal.payback_day_for_buyer, self.date_datetime)

    def test_add_payback_day_for_buyer_1day(self):
        pay_order_obj = self.create_pay_order_obj()
        pay_order_obj.deal.postponement_pay_for_buyer = 1
        pay_order_obj.add_payback_day_for_buyer(self.pay_order_dataclass.date)
        date_plus_one_day = self.date_datetime + timedelta(days=self.deal.postponement_pay_for_us)
        self.assertEqual(pay_order_obj.deal.payback_day_for_buyer, date_plus_one_day)

    def test_add_or_replay_deal_debt(self):
        pay_order_obj = self.create_pay_order_obj()
        pay_order_obj.add_or_replay_deal_debt()
        self.assertEqual(pay_order_obj.deal.deal_our_debt_UPD, 1000000)
        self.assertNotEqual(pay_order_obj.deal.deal_our_debt_UPD, self.deal_our_debt_UPD)

    def test_compare_UPD_and_payments_small_zero(self):
        pay_order_dataclass = self.create_payorder_dataclass()
        compare_UPD_and_payments(
            self.deal,
            self.deal.seller,
            pay_order_dataclass,
        )
        self.assertEqual(self.deal.deal_our_debt_UPD, pay_order_dataclass.pay_quantity)
        if isinstance(pay_order_dataclass.pay_quantity, float):
            self.assertEqual(self.deal.deal_our_pay_amount, (0 - pay_order_dataclass.pay_quantity))
        else:
            self.fail()

        client_type = 'buyer'
        doc_type = 'UPD_outgoing'
        pay_order_dataclass = self.create_payorder_dataclass(client_type, doc_type)
        compare_UPD_and_payments(
            self.deal,
            self.deal.buyer,
            pay_order_dataclass,
        )
        self.assertEqual(self.deal.deal_buyer_debt_UPD, pay_order_dataclass.pay_quantity)
        if isinstance(pay_order_dataclass.pay_quantity, float):
            self.assertEqual(self.deal.deal_buyer_pay_amount, (0 - pay_order_dataclass.pay_quantity))
        else:
            self.fail()

        client_type = 'logic'
        doc_type = 'UPD_logic'
        pay_order_dataclass = self.create_payorder_dataclass(client_type, doc_type)
        compare_UPD_and_payments(
            self.deal,
            self.deal.current_logic,
            pay_order_dataclass,
        )
        self.assertEqual(self.deal.logic_our_debt_UPD, pay_order_dataclass.pay_quantity)
        if isinstance(pay_order_dataclass.pay_quantity, float):
            self.assertEqual(self.deal.logic_our_pay_amount, (0 - pay_order_dataclass.pay_quantity))
        else:
            self.fail()

        client_type = 'logic'
        doc_type = 'UPD_outgoing'
        self.assertRaises(serializers.ValidationError, self.create_payorder_dataclass, client_type, doc_type)

    def test_compare_UPD_and_payments_equal(self):
        pay_order_dataclass = self.create_payorder_dataclass()
        self.deal.deal_our_pay_amount = 1000000
        compare_UPD_and_payments(
            self.deal,
            self.deal.seller,
            pay_order_dataclass,
        )
        self.assertEqual(self.deal.deal_our_pay_amount, 0)

        client_type = 'buyer'
        doc_type = 'UPD_outgoing'
        pay_order_dataclass = self.create_payorder_dataclass(client_type, doc_type)
        self.deal.deal_buyer_pay_amount = 1000000
        compare_UPD_and_payments(
            self.deal,
            self.deal.buyer,
            pay_order_dataclass,
        )
        self.assertEqual(self.deal.deal_buyer_pay_amount, 0)

        client_type = 'logic'
        doc_type = 'UPD_logic'
        pay_order_dataclass = self.create_payorder_dataclass(client_type, doc_type)
        self.deal.logic_our_pay_amount = 1000000
        compare_UPD_and_payments(
            self.deal,
            self.deal.current_logic,
            pay_order_dataclass,
        )
        self.assertEqual(self.deal.logic_our_pay_amount, 0)

    def test_compare_UPD_and_payments_bigger(self):
        pay_order_dataclass = self.create_payorder_dataclass()
        old_tail = self.balance.tails.current_tail_form_one
        old_tail_active = self.balance.tails.active_tails_form_one
        self.deal.deal_our_pay_amount = 3000000
        compare_UPD_and_payments(
            self.deal,
            self.deal.seller,
            pay_order_dataclass,
        )
        delta = 3000000 - pay_order_dataclass.pay_quantity
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
        self.assertEqual(self.deal.deal_our_pay_amount, 0)
        self.assertEqual(tails.current_tail_form_one, old_tail + delta)
        self.assertEqual(tails.active_tails_form_one, old_tail_active + 1)
        # self.assertEqual(self.deal.seller.tails.data_number_json.values(), ([(asdict(pay_order_dataclass))],))

    def test_compare_UPD_and_payments_seller_bigger_cash(self):
        pay_order_dataclass = self.create_payorder_dataclass()
        old_tail = self.balance.tails.current_tail_form_two
        old_tail_active = self.balance.tails.active_tails_form_two
        self.deal.deal_our_pay_amount = 3000000
        self.deal.cash = True
        compare_UPD_and_payments(
            self.deal,
            self.deal.seller,
            pay_order_dataclass,
        )
        cur_tail = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
        delta = 3000000 - pay_order_dataclass.pay_quantity
        self.assertEqual(self.deal.deal_our_pay_amount, 0)
        self.assertEqual(cur_tail.current_tail_form_one, old_tail + delta)
        self.assertEqual(cur_tail.active_tails_form_one, old_tail_active + 1)

    def test_delta_UPD_send_message(self):
        _ = self.create_payorder_dataclass()
        delta = 100
        text_val = 3
        client = self.deal.seller
        instance = self.deal
        # delta_UPD_send_message(delta, text_val, client, instance)
        self.assertRaises(ValueError, delta_UPD_send_message, delta, text_val, client, instance, self.deal.entity)
        # self.assertTrue(MessageToUserEggs.objects.all()) #TODO
        # self.assertTrue(self.get_message())

    def test_add_or_replay_deal_debt_logic_application(self):
        pay_order_dataclass = self.create_payorder_dataclass(doc_type='application_contract_logic', client_type='logic')
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.current_logic,
        )
        pay_order_obj.add_or_replay_deal_debt()

        self.assertEqual(pay_order_obj.deal.logic_our_debt_for_app_contract, pay_order_dataclass.pay_quantity)
        self.assertEqual(pay_order_obj.deal.delivery_cost, pay_order_dataclass.pay_quantity)
        self.assertEqual(self.deal.logic_our_debt_for_app_contract, pay_order_dataclass.pay_quantity)
        self.assertEqual(self.deal.delivery_cost, pay_order_dataclass.pay_quantity)


    def test_add_or_replay_deal_debt_logic_payment(self):
        pay_order_dataclass = self.create_payorder_dataclass(doc_type='payment_order_outcoming_logic', client_type='logic')
        upd_pay = 2000000
        cur_pay = -2000000
        self.deal.logic_our_debt_UPD = upd_pay
        self.deal.logic_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.current_logic,
        )
        self.assertEqual(pay_order_obj.deal.logic_our_pay_amount, cur_pay)
        self.assertEqual(self.deal.logic_our_pay_amount, cur_pay)
        pay_order_obj.add_or_replay_deal_debt()
        self.assertEqual(pay_order_obj.deal.logic_our_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)
        self.assertEqual(self.deal.logic_our_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)

    def test_add_or_replay_deal_debt_logic_payment_sub_zero_force(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '1000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming_logic',
            client_type='logic',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        self.deal.logic_our_debt_UPD = upd_pay
        self.deal.logic_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.current_logic,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0

        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)

        self.assertEqual(pay_order_obj.deal.logic_our_pay_amount, 0)
        self.assertEqual(self.deal.logic_our_pay_amount, 0)
        self.assertTrue(tails.data_number_json)
        self.assertEqual(tails.current_tail_form_one, abs(abs(cur_pay) - float(cur_pay_quantity)))
        self.assertEqual(tails.active_tails_form_one, 1)

    def test_add_or_replay_deal_debt_logic_payment_delta_positive(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '200000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming_logic',
            client_type='logic',
            pay_quantity=cur_pay_quantity,
        )
        self.deal.logic_our_debt_UPD = upd_pay
        self.deal.logic_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.current_logic,
        )
        pay_order_obj.add_or_replay_deal_debt()
        self.assertEqual(pay_order_obj.deal.logic_our_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)
        self.assertEqual(self.deal.logic_our_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)

    def test_add_or_replay_deal_debt_logic_payment_sub_zero_force_cash(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '1000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming_logic',
            client_type='logic',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        self.deal.delivery_form_payment = 3
        self.deal.logic_our_debt_UPD = upd_pay
        self.deal.logic_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.current_logic,
        )
        self.balance.tails.current_tail_form_two = 0
        self.balance.tails.active_tails_form_two = 0

        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)

        self.assertEqual(pay_order_obj.deal.logic_our_pay_amount, 0)
        self.assertEqual(self.deal.logic_our_pay_amount, 0)
        self.assertFalse(tails.data_number_json)
        self.assertTrue(tails.data_number_json_cash)
        self.assertEqual(tails.current_tail_form_two, abs(abs(cur_pay) - float(cur_pay_quantity)))
        self.assertEqual(tails.active_tails_form_two, 1)
        self.assertEqual(tails.current_tail_form_one, 0)
        self.assertEqual(tails.active_tails_form_one, 0)

    def test_add_or_replay_deal_debt_logic_payment_sub_zero_not_force(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '1000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming_logic',
            client_type='logic',
            pay_quantity=cur_pay_quantity,
        )
        self.deal.logic_our_debt_UPD = upd_pay
        self.deal.logic_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.current_logic,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0
        self.assertRaises(serializers.ValidationError, pay_order_obj.add_or_replay_deal_debt)

    def test_add_or_replay_deal_debt_seller_payment(self):
        pay_order_dataclass = self.create_payorder_dataclass(doc_type='payment_order_outcoming', client_type='seller')
        upd_pay = 2000000
        cur_pay = -2000000
        self.deal.deal_our_debt_UPD = upd_pay
        self.deal.deal_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.seller,
        )
        self.assertEqual(pay_order_obj.deal.deal_our_pay_amount, cur_pay)
        self.assertEqual(self.deal.deal_our_pay_amount, cur_pay)
        pay_order_obj.add_or_replay_deal_debt()
        delta = pay_order_obj.deal.deal_our_pay_amount - pay_order_dataclass.pay_quantity
        self.assertEqual(pay_order_obj.deal.deal_our_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)
        self.assertEqual(self.deal.deal_our_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)

    def test_add_or_replay_deal_debt_seller_payment_delta_positive(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '200000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming',
            client_type='seller',
            pay_quantity=cur_pay_quantity,
        )
        self.deal.deal_our_debt_UPD = upd_pay
        self.deal.deal_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.seller,
        )
        pay_order_obj.add_or_replay_deal_debt()
        self.assertEqual(pay_order_obj.deal.deal_our_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)
        self.assertEqual(self.deal.deal_our_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)

    def test_add_or_replay_deal_debt_seller_payment_sub_zero_force(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '1000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming',
            client_type='seller',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        self.deal.deal_our_debt_UPD = upd_pay
        self.deal.deal_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.seller,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0

        pay_order_obj.add_or_replay_deal_debt()

        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)

        self.assertEqual(pay_order_obj.deal.deal_our_pay_amount, 0)
        self.assertEqual(self.deal.deal_our_pay_amount, 0)
        self.assertTrue(tails.data_number_json)
        self.assertEqual(tails.current_tail_form_one, abs(abs(cur_pay) - float(cur_pay_quantity)))
        self.assertEqual(tails.active_tails_form_one, 1)

    def test_add_or_replay_deal_debt_seller_payment_sub_zero_not_force(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '1000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming',
            client_type='seller',
            pay_quantity=cur_pay_quantity,
        )
        self.deal.deal_our_debt_UPD = upd_pay
        self.deal.deal_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.seller,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0
        self.assertRaises(serializers.ValidationError, pay_order_obj.add_or_replay_deal_debt)

    def test_add_or_replay_deal_debt_buyer_payment(self):
        pay_order_dataclass = self.create_payorder_dataclass(doc_type='payment_order_incoming', client_type='buyer')
        upd_pay = 2000000
        cur_pay = -2000000
        self.deal.deal_buyer_debt_UPD = upd_pay
        self.deal.deal_buyer_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.buyer,
        )
        self.assertEqual(pay_order_obj.deal.deal_buyer_pay_amount, cur_pay)
        self.assertEqual(self.deal.deal_buyer_pay_amount, cur_pay)
        pay_order_obj.add_or_replay_deal_debt()
        delta = pay_order_obj.deal.deal_buyer_pay_amount - pay_order_dataclass.pay_quantity
        self.assertEqual(pay_order_obj.deal.deal_buyer_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)
        self.assertEqual(self.deal.deal_buyer_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)

    def test_add_or_replay_deal_debt_buyer_payment_sub_zero_force(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '1000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_incoming',
            client_type='buyer',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        self.deal.deal_buyer_debt_UPD = upd_pay
        self.deal.deal_buyer_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.buyer,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0

        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
        self.assertEqual(pay_order_obj.deal.deal_our_pay_amount, 0)
        self.assertEqual(self.deal.deal_our_pay_amount, 0)
        self.assertTrue(tails.data_number_json)
        self.assertEqual(tails.current_tail_form_one, abs(abs(cur_pay) - float(cur_pay_quantity)))
        self.assertEqual(tails.active_tails_form_one, 1)

    def test_add_or_replay_deal_debt_buyer_payment_delta_positive(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '200000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_incoming',
            client_type='buyer',
            pay_quantity=cur_pay_quantity,
        )
        self.deal.deal_buyer_debt_UPD = upd_pay
        self.deal.deal_buyer_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.buyer,
        )
        pay_order_obj.add_or_replay_deal_debt()
        self.assertEqual(pay_order_obj.deal.deal_buyer_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)
        self.assertEqual(self.deal.deal_buyer_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)

    def test_add_or_replay_deal_debt_buyer_payment_sub_zero_force_cash(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '1000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_incoming',
            client_type='buyer',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        self.deal.cash = True
        self.deal.deal_buyer_debt_UPD = upd_pay
        self.deal.deal_buyer_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.buyer,
        )
        self.balance.tails.current_tail_form_two = 0
        self.balance.tails.active_tails_form_two = 0

        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)

        self.assertEqual(pay_order_obj.deal.deal_our_pay_amount, 0)
        self.assertEqual(self.deal.deal_our_pay_amount, 0)
        self.assertFalse(tails.data_number_json)
        self.assertTrue(tails.data_number_json_cash)
        self.assertEqual(tails.current_tail_form_two, abs(abs(cur_pay) - float(cur_pay_quantity)))
        self.assertEqual(tails.active_tails_form_two, 1)
        self.assertEqual(tails.current_tail_form_one, 0)
        self.assertEqual(tails.active_tails_form_one, 0)

    def test_add_or_replay_deal_debt_buyer_payment_sub_zero_not_force(self):
        upd_pay = 2000000
        cur_pay = -500000
        cur_pay_quantity = '1000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_incoming',
            client_type='buyer',
            pay_quantity=cur_pay_quantity,
        )
        self.deal.deal_buyer_debt_UPD = upd_pay
        self.deal.deal_buyer_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.buyer,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0
        self.assertRaises(serializers.ValidationError, pay_order_obj.add_or_replay_deal_debt)

    def test_add_or_replay_deal_debt_buyer_tail(self): #TODO
        pay_order_dataclass = self.create_payorder_dataclass(doc_type='tail_payment', client_type='buyer')
        upd_pay = 2000000
        cur_pay = -2000000
        self.deal.deal_buyer_debt_UPD = upd_pay
        self.deal.deal_buyer_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.buyer,
        )
        self.assertEqual(pay_order_obj.deal.deal_buyer_pay_amount, cur_pay)
        self.assertEqual(self.deal.deal_buyer_pay_amount, cur_pay)
        pay_order_obj.add_or_replay_deal_debt()
        delta = pay_order_obj.deal.deal_buyer_pay_amount - pay_order_dataclass.pay_quantity
        self.assertEqual(pay_order_obj.deal.deal_buyer_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)

    def test_add_or_replay_deal_debt_buyer_payment_sub_zero_not_UPD(self):
        cur_pay = -500000
        cur_pay_quantity = '5000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_incoming',
            client_type='buyer',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        inital_payments_amount = (
            self.deal.cB_white*self.deal.buyer_cB_white_cost +
            self.deal.cB_cream*self.deal.buyer_cB_cream_cost +
            self.deal.cB_brown*self.deal.buyer_cB_brown_cost +
            self.deal.c0_white*self.deal.buyer_c0_white_cost +
            self.deal.c0_cream*self.deal.buyer_c0_cream_cost +
            self.deal.c0_brown*self.deal.buyer_c0_brown_cost +
            self.deal.c1_white*self.deal.buyer_c1_white_cost +
            self.deal.c1_cream*self.deal.buyer_c1_cream_cost +
            self.deal.c1_brown*self.deal.buyer_c1_brown_cost +
            self.deal.c2_white*self.deal.buyer_c2_white_cost +
            self.deal.c2_cream*self.deal.buyer_c2_cream_cost +
            self.deal.c2_brown*self.deal.buyer_c2_brown_cost +
            self.deal.c3_white*self.deal.buyer_c3_white_cost +
            self.deal.c3_cream*self.deal.buyer_c3_cream_cost +
            self.deal.c3_brown*self.deal.buyer_c3_brown_cost +
            self.deal.dirt*self.deal.buyer_dirt_cost
        )
        # add_exp_and_delivery_cost = self.deal.additional_expense.expense_total + self.deal.delivery_cost
        # inital_payments_amount += add_exp_and_delivery_cost
        self.deal.deal_buyer_pay_amount = cur_pay
        self.deal.deal_buyer_debt_UPD = 0
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.buyer,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0
        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
        self.assertFalse(pay_order_obj.deal.deal_buyer_debt_UPD)
        self.assertEqual(pay_order_obj.deal.deal_buyer_pay_amount, inital_payments_amount)
        self.assertEqual(self.deal.deal_buyer_pay_amount, inital_payments_amount)
        self.assertTrue(tails.data_number_json)
        self.assertEqual(
            tails.current_tail_form_one,
            pay_order_dataclass.pay_quantity - (inital_payments_amount - abs(cur_pay))
        )
        self.assertEqual(tails.active_tails_form_one, 1)

    def test_add_or_replay_deal_debt_buyer_payment_sub_zero_not_UPD_cash(self):
        cur_pay = -500000
        cur_pay_quantity = '5000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_incoming',
            client_type='buyer',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        self.deal.cash = True
        inital_payments_amount = (
            self.deal.cB_white*self.deal.buyer_cB_white_cost +
            self.deal.cB_cream*self.deal.buyer_cB_cream_cost +
            self.deal.cB_brown*self.deal.buyer_cB_brown_cost +
            self.deal.c0_white*self.deal.buyer_c0_white_cost +
            self.deal.c0_cream*self.deal.buyer_c0_cream_cost +
            self.deal.c0_brown*self.deal.buyer_c0_brown_cost +
            self.deal.c1_white*self.deal.buyer_c1_white_cost +
            self.deal.c1_cream*self.deal.buyer_c1_cream_cost +
            self.deal.c1_brown*self.deal.buyer_c1_brown_cost +
            self.deal.c2_white*self.deal.buyer_c2_white_cost +
            self.deal.c2_cream*self.deal.buyer_c2_cream_cost +
            self.deal.c2_brown*self.deal.buyer_c2_brown_cost +
            self.deal.c3_white*self.deal.buyer_c3_white_cost +
            self.deal.c3_cream*self.deal.buyer_c3_cream_cost +
            self.deal.c3_brown*self.deal.buyer_c3_brown_cost +
            self.deal.dirt*self.deal.buyer_dirt_cost
        )
        self.deal.deal_buyer_pay_amount = cur_pay
        self.deal.deal_buyer_debt_UPD = 0
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.buyer,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0
        self.balance.tails.current_tail_form_two = 0
        self.balance.tails.active_tails_form_two = 0
        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
        self.assertFalse(tails.current_tail_form_one)
        self.assertFalse(tails.active_tails_form_one)
        self.assertFalse(pay_order_obj.deal.deal_buyer_debt_UPD)
        self.assertEqual(pay_order_obj.deal.deal_buyer_pay_amount, inital_payments_amount)
        self.assertEqual(self.deal.deal_buyer_pay_amount, inital_payments_amount)
        self.assertTrue(tails.data_number_json_cash)
        self.assertFalse(tails.data_number_json)
        self.assertEqual(
            tails.current_tail_form_two,
            pay_order_dataclass.pay_quantity - (inital_payments_amount - abs(cur_pay))
        )
        self.assertEqual(tails.active_tails_form_two, 1)

    def test_add_or_replay_deal_debt_seller_payment_sub_zero_not_UPD_cash(self):
        cur_pay = -500000
        cur_pay_quantity = '5000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming',
            client_type='seller',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        self.deal.cash = True
        inital_payments_amount = (
            self.deal.cB_white*self.deal.seller_cB_white_cost +
            self.deal.cB_cream*self.deal.seller_cB_cream_cost +
            self.deal.cB_brown*self.deal.seller_cB_brown_cost +
            self.deal.c0_white*self.deal.seller_c0_white_cost +
            self.deal.c0_cream*self.deal.seller_c0_cream_cost +
            self.deal.c0_brown*self.deal.seller_c0_brown_cost +
            self.deal.c1_white*self.deal.seller_c1_white_cost +
            self.deal.c1_cream*self.deal.seller_c1_cream_cost +
            self.deal.c1_brown*self.deal.seller_c1_brown_cost +
            self.deal.c2_white*self.deal.seller_c2_white_cost +
            self.deal.c2_cream*self.deal.seller_c2_cream_cost +
            self.deal.c2_brown*self.deal.seller_c2_brown_cost +
            self.deal.c3_white*self.deal.seller_c3_white_cost +
            self.deal.c3_cream*self.deal.seller_c3_cream_cost +
            self.deal.c3_brown*self.deal.seller_c3_brown_cost +
            self.deal.dirt*self.deal.seller_dirt_cost
        )
        # add_exp_and_delivery_cost = self.deal.additional_expense.expense_total + self.deal.delivery_cost
        # inital_payments_amount += add_exp_and_delivery_cost
        self.deal.deal_our_pay_amount = cur_pay
        self.deal.deal_our_debt_UPD = 0
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.seller,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0
        self.balance.tails.current_tail_form_two = 0
        self.balance.tails.active_tails_form_two = 0
        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
        self.assertFalse(pay_order_obj.deal.deal_our_debt_UPD)
        self.assertFalse(pay_order_obj.deal.seller.cur_balance.last().tails.current_tail_form_two)
        self.assertFalse(pay_order_obj.deal.seller.cur_balance.last().tails.active_tails_form_two)
        self.assertEqual(pay_order_obj.deal.deal_our_pay_amount, inital_payments_amount)
        self.assertEqual(self.deal.deal_our_pay_amount, inital_payments_amount)
        self.assertTrue(tails.data_number_json)
        self.assertFalse(tails.data_number_json_cash)
        self.assertEqual(
            tails.current_tail_form_one,
            pay_order_dataclass.pay_quantity - (inital_payments_amount - abs(cur_pay))
        )
        self.assertEqual(tails.active_tails_form_one, 1)

    def test_add_or_replay_deal_debt_seller_payment_sub_zero_not_UPD(self):
        cur_pay = -500000
        cur_pay_quantity = '5000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming',
            client_type='seller',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        inital_payments_amount = (
            self.deal.cB_white*self.deal.seller_cB_white_cost +
            self.deal.cB_cream*self.deal.seller_cB_cream_cost +
            self.deal.cB_brown*self.deal.seller_cB_brown_cost +
            self.deal.c0_white*self.deal.seller_c0_white_cost +
            self.deal.c0_cream*self.deal.seller_c0_cream_cost +
            self.deal.c0_brown*self.deal.seller_c0_brown_cost +
            self.deal.c1_white*self.deal.seller_c1_white_cost +
            self.deal.c1_cream*self.deal.seller_c1_cream_cost +
            self.deal.c1_brown*self.deal.seller_c1_brown_cost +
            self.deal.c2_white*self.deal.seller_c2_white_cost +
            self.deal.c2_cream*self.deal.seller_c2_cream_cost +
            self.deal.c2_brown*self.deal.seller_c2_brown_cost +
            self.deal.c3_white*self.deal.seller_c3_white_cost +
            self.deal.c3_cream*self.deal.seller_c3_cream_cost +
            self.deal.c3_brown*self.deal.seller_c3_brown_cost +
            self.deal.dirt*self.deal.seller_dirt_cost
        )
        # add_exp_and_delivery_cost = self.deal.additional_expense.expense_total + self.deal.delivery_cost
        # inital_payments_amount += add_exp_and_delivery_cost
        self.deal.deal_our_pay_amount = cur_pay
        self.deal.deal_our_debt_UPD = 0
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.seller,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0
        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
        self.assertFalse(pay_order_obj.deal.deal_our_debt_UPD)
        self.assertEqual(pay_order_obj.deal.deal_our_pay_amount, inital_payments_amount)
        self.assertEqual(self.deal.deal_our_pay_amount, inital_payments_amount)
        self.assertTrue(tails.data_number_json)
        self.assertEqual(
            tails.current_tail_form_one,
            pay_order_dataclass.pay_quantity - (inital_payments_amount - abs(cur_pay))
        )
        self.assertEqual(tails.active_tails_form_one, 1)

    def test_add_or_replay_deal_debt_seller_payment_positive_not_UPD(self):
        cur_pay = -500000
        cur_pay_quantity = '300000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming',
            client_type='seller',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        inital_payments_amount = (
            self.deal.cB_white*self.deal.seller_cB_white_cost +
            self.deal.cB_cream*self.deal.seller_cB_cream_cost +
            self.deal.cB_brown*self.deal.seller_cB_brown_cost +
            self.deal.c0_white*self.deal.seller_c0_white_cost +
            self.deal.c0_cream*self.deal.seller_c0_cream_cost +
            self.deal.c0_brown*self.deal.seller_c0_brown_cost +
            self.deal.c1_white*self.deal.seller_c1_white_cost +
            self.deal.c1_cream*self.deal.seller_c1_cream_cost +
            self.deal.c1_brown*self.deal.seller_c1_brown_cost +
            self.deal.c2_white*self.deal.seller_c2_white_cost +
            self.deal.c2_cream*self.deal.seller_c2_cream_cost +
            self.deal.c2_brown*self.deal.seller_c2_brown_cost +
            self.deal.c3_white*self.deal.seller_c3_white_cost +
            self.deal.c3_cream*self.deal.seller_c3_cream_cost +
            self.deal.c3_brown*self.deal.seller_c3_brown_cost +
            self.deal.dirt*self.deal.seller_dirt_cost
        )
        # add_exp_and_delivery_cost = self.deal.additional_expense.expense_total + self.deal.delivery_cost
        # inital_payments_amount += add_exp_and_delivery_cost
        self.deal.deal_our_pay_amount = cur_pay
        self.deal.deal_our_debt_UPD = 0
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.seller,
        )
        pay_order_obj.add_or_replay_deal_debt()

        self.assertFalse(pay_order_obj.deal.deal_our_debt_UPD)
        self.assertEqual(pay_order_obj.deal.deal_our_pay_amount, cur_pay + pay_order_dataclass.pay_quantity)

    def test_add_or_replay_deal_debt_seller_payment_sub_zero_not_UPD_not_force(self):
        cur_pay = -500000
        cur_pay_quantity = '5000000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming',
            client_type='seller',
            pay_quantity=cur_pay_quantity,
        )
        self.deal.deal_our_pay_amount = cur_pay
        self.deal.deal_our_debt_UPD = 0
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.seller,
        )
        self.assertRaises(serializers.ValidationError, pay_order_obj.add_or_replay_deal_debt)

    def test_add_or_replay_deal_debt_logic_payment_sub_zero_not_UPD(self):
        cur_pay = -50000
        cur_pay_quantity = '300000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming_logic',
            client_type='logic',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        self.deal.delivery_cost = 200000
        self.deal.logic_our_debt_UPD = 0
        self.deal.logic_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.current_logic,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0
        inital_payments_amount = self.deal.delivery_cost
        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)

        self.assertFalse(pay_order_obj.deal.logic_our_debt_UPD)
        self.assertEqual(pay_order_obj.deal.logic_our_pay_amount, inital_payments_amount)
        self.assertEqual(self.deal.logic_our_pay_amount, inital_payments_amount)
        self.assertTrue(tails.data_number_json)
        self.assertEqual(
            tails.current_tail_form_one,
            pay_order_dataclass.pay_quantity - (inital_payments_amount - abs(cur_pay))
        )
        self.assertEqual(tails.active_tails_form_one, 1)

    def test_add_or_replay_deal_debt_logic_payment_sub_zero_not_UPD_cash(self):
        cur_pay = -50000
        cur_pay_quantity = '300000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming_logic',
            client_type='logic',
            pay_quantity=cur_pay_quantity,
            force_bool=True,
        )
        self.deal.delivery_form_payment = 3
        self.deal.delivery_cost = 200000
        self.deal.logic_our_debt_UPD = 0
        self.deal.logic_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.current_logic,
        )
        self.balance.tails.current_tail_form_one = 0
        self.balance.tails.active_tails_form_one = 0
        self.balance.tails.current_tail_form_two = 0
        self.balance.tails.active_tails_form_two = 0
        inital_payments_amount = self.deal.delivery_cost
        pay_order_obj.add_or_replay_deal_debt()
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)

        self.assertFalse(pay_order_obj.deal.logic_our_debt_UPD)
        self.assertFalse(tails.current_tail_form_one)
        self.assertFalse(tails.active_tails_form_one)
        self.assertEqual(pay_order_obj.deal.logic_our_pay_amount, inital_payments_amount)
        self.assertEqual(self.deal.logic_our_pay_amount, inital_payments_amount)
        self.assertTrue(tails.data_number_json_cash)
        self.assertFalse(tails.data_number_json)
        self.assertEqual(
            tails.current_tail_form_two,
            pay_order_dataclass.pay_quantity - (inital_payments_amount - abs(cur_pay))
        )
        self.assertEqual(tails.active_tails_form_two, 1)

    def test_add_or_replay_deal_debt_logic_payment_sub_zero_not_UPD_to_many(self):
        cur_pay = -50000
        cur_pay_quantity = '300000'
        pay_order_dataclass = self.create_payorder_dataclass(
            doc_type='payment_order_outcoming_logic',
            client_type='logic',
            pay_quantity=cur_pay_quantity,
        )
        self.deal.delivery_form_payment = 3
        self.deal.delivery_cost = 200000
        self.deal.logic_our_debt_UPD = 0
        self.deal.logic_our_pay_amount = cur_pay
        pay_order_obj = DealPayOrderUPDservice(
            data_detail = pay_order_dataclass,
            current_deal = self.deal,
            pay_client = self.deal.current_logic,
        )
        tails = TailsContragentModelEggs.objects.get(pk=self.balance.tails.pk)
        tails.current_tail_form_one = 0
        tails.active_tails_form_one = 0
        tails.current_tail_form_two = 0
        tails.active_tails_form_two = 0

        self.assertRaises(serializers.ValidationError, pay_order_obj.add_or_replay_deal_debt)







