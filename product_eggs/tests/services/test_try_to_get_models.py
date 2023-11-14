from django.test import TestCase
from rest_framework import serializers

from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.services.get_anything.get_managers import get_managers
from product_eggs.tests.create_models import TestModelCreator
from product_eggs.services.get_anything.try_to_get_models import (
    get_client_for_inn, get_client_for_tail_pk, try_to_get_deal_docs_model,
    try_to_get_deal_model, try_to_get_deal_model_for_doc_deal_id,
)
from users.models import CustomUser


class TestGetModels(TestCase):

    def test_get_client_for_inn_buyer(self):
        test_obj = TestModelCreator()
        buyer = test_obj.create_buyer()
        client = get_client_for_inn(buyer.inn, 'buyer')
        if client:
            self.assertIs(type(client), BuyerCardEggs)
            self.assertEqual(buyer.inn, client.inn)
        else:
            self.fail()

    def test_get_client_for_inn_seller(self):
        test_obj = TestModelCreator()
        seller = test_obj.create_seller()
        client = get_client_for_inn(seller.inn, 'seller')
        if client:
            self.assertIs(type(client), SellerCardEggs)
            self.assertEqual(seller.inn, client.inn)
        else:
            self.fail()

    def test_get_client_for_inn_logic(self):
        test_obj = TestModelCreator()
        logic = test_obj.create_logic()
        client = get_client_for_inn(logic.inn, 'logic')
        if client:
            self.assertIs(type(client), LogicCardEggs)
            self.assertEqual(logic.inn, client.inn)
        else:
            self.fail()

    def test_get_client_for_tail_pk_seller(self):
        test_obj = TestModelCreator()
        seller = test_obj.create_seller()
        bal = test_obj.create_balance(client=seller)
        client = get_client_for_tail_pk(bal.tails.pk)
        self.assertIs(type(client), SellerCardEggs)

    def test_get_client_for_tail_pk_buyer(self):
        test_obj = TestModelCreator()
        buyer = test_obj.create_buyer()
        bal = test_obj.create_balance(client=buyer)
        client = get_client_for_tail_pk(bal.tails.pk)
        self.assertIs(type(client), BuyerCardEggs)

    # def test_get_client_for_tail_pk_fail(self):
    #     get_client_for_tail_pk(1019291)
    #     self.assertRaises(serializers.ValidationError)

    def test_try_to_get_deal_model(self):
        test_obj = TestModelCreator()
        deal = test_obj.create_base_deal()
        cur_model = try_to_get_deal_model(deal.pk)
        self.assertIs(type(cur_model), BaseDealEggsModel)
        self.assertEqual(deal.pk, cur_model.pk)

    def test_try_to_get_deal_model_for_doc_deal_id(self):
        test_obj = TestModelCreator()
        deal = test_obj.create_base_deal()
        cur_model = try_to_get_deal_model_for_doc_deal_id(deal.documents.pk)
        self.assertIs(type(cur_model), BaseDealEggsModel)
        self.assertEqual(deal.pk, cur_model.pk)

    def test_try_to_get_deal_docs_model(self):
        test_obj = TestModelCreator()
        deal_docs = test_obj.create_deal_docs()
        cur_model = try_to_get_deal_docs_model(deal_docs.pk)
        self.assertIs(type(cur_model), DocumentsDealEggsModel)
        self.assertEqual(deal_docs.pk, cur_model.pk)

    def test_get_managers(self):
        test_obj = TestModelCreator()
        seller = test_obj.create_seller()
        buyer = test_obj.create_buyer()
        result = get_managers(seller.inn, buyer.inn)
        self.assertIs(type(result), list)
        self.assertEqual(result, [seller.manager, buyer.manager])
        self.assertIs(type(result[0]), CustomUser)
        self.assertIs(type(result[1]), CustomUser)
        self.assertEqual(result[0], seller.manager)
        self.assertEqual(result[1], buyer.manager)


















