from django.test import TestCase

from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.balance import (
    get_balance_for_tail, get_balance_for_tail_pk,
    get_cur_balance, get_new_balance_model
)
from product_eggs.tests.create_models import TestModelCreator


class TestBalaceService(TestCase):

    def test_get_new_balance_model(self):
        test_obj = TestModelCreator()
        seller = test_obj.create_seller()
        buyer = test_obj.create_buyer()
        logic = test_obj.create_logic()
        res_1 = get_new_balance_model('5612163931', seller)
        self.assertIs(type(res_1), BalanceBaseClientEggs)
        self.assertEqual(seller.cur_balance.all()[0].client_seller, seller)
        self.assertEqual(res_1.client_seller, seller)
        self.assertEqual(res_1.entity.inn, '5612163931')
        self.assertEqual(res_1.entity.name, 'Пилигрим')
        res_2 = get_new_balance_model('5612163931', buyer)
        self.assertIs(type(res_2), BalanceBaseClientEggs)
        self.assertEqual(buyer.cur_balance.all()[0].client_buyer, buyer)
        self.assertEqual(res_2.client_buyer, buyer)
        res_3 = get_new_balance_model('5612163931', logic)
        self.assertIs(type(res_3), BalanceBaseClientEggs)
        self.assertEqual(logic.cur_balance.all()[0].client_logic, logic)
        self.assertEqual(res_3.client_logic, logic)
        self.assertRaises(KeyError, get_new_balance_model, 'piligrimO', seller)

    def test_get_cur_balance(self):
        test_obj = TestModelCreator()
        seller = test_obj.create_seller()
        buyer = test_obj.create_buyer()
        logic = test_obj.create_logic()
        bal1 = get_new_balance_model('5612163931', seller)
        bal2 = get_new_balance_model('5612163931', buyer)
        bal3 = get_new_balance_model('5612163931', logic)
        res1 = get_cur_balance('5612163931', seller)
        self.assertEqual(bal1, res1)
        entity = test_obj.create_entity()
        self.assertRaises(KeyError, get_cur_balance, entity, buyer)
        # self.assertRaises(AttributeError, get_cur_balance, 'piligrim', entity)

    def test_get_balance_for_tail(self):
        test_obj = TestModelCreator()
        seller = test_obj.create_seller()
        bal = test_obj.create_balance(seller)
        if bal.tails:
          self.assertEqual(get_balance_for_tail(bal.tails), bal)
          self.assertTrue(bal.tails.pk)
          res_tail = TailsContragentModelEggs.objects.get(pk=bal.tails.pk)
          self.assertEqual(bal.tails, res_tail)
          self.assertEqual(get_balance_for_tail(bal.tails), bal)
          # self.assertEqual(get_balance_for_tail(res_tail), bal) TODO
          # res_2 = get_balance_for_tail_pk(bal.tails.pk)
          # self.assertEqual(res_2, bal)

    def test_get_balance_for_tail_pk(self):
        test_obj = TestModelCreator()
        seller = test_obj.create_seller()
        bal = test_obj.create_balance(seller)
        if bal.tails:
          res = get_balance_for_tail_pk(bal.tails.pk)
          self.assertEqual(res, bal)
          res_w = get_balance_for_tail_pk('s')








