from django.test import TestCase
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.comment import CommentEggs
from product_eggs.models.documents import DocumentsContractEggsModel, DocumentsDealEggsModel
from product_eggs.models.entity import EntityEggs
from product_eggs.models.origins import OriginsDealEggs
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.tests.create_models import TestModelCreator
from users.models import CustomUser


class TestCreateModels(TestCase):

    def test_create_requisites(self):
        test_obj = TestModelCreator()
        result = test_obj.create_requisites()
        self.assertTrue(result, RequisitesEggs)
        self.assertIs(type(result), RequisitesEggs)

    def test_create_entity(self):
        test_obj = TestModelCreator()
        result = test_obj.create_entity()
        self.assertTrue(result, EntityEggs)
        self.assertIs(type(result), EntityEggs)

    def test_create_balance(self):
        test_obj = TestModelCreator()
        result = test_obj.create_balance(client=test_obj.create_seller())
        self.assertTrue(result, BalanceBaseClientEggs)
        self.assertIs(type(result), BalanceBaseClientEggs)
        self.assertFalse(result.client_buyer)
        self.assertTrue(result.client_seller)
        self.assertFalse(result.client_logic)
        seller=test_obj.create_seller()
        res_1 = test_obj.create_balance(client=seller)
        self.assertEqual(res_1.client_seller, seller)

    def test_create_docs_origin(self):
        test_obj = TestModelCreator()
        result = test_obj.create_docs_origin()
        self.assertTrue(result, OriginsDealEggs)

    def test_create_randomletter(self):
        test_obj = TestModelCreator()
        result = test_obj.create_randletter()
        self.assertTrue(result, str)

    def test_create_random_username(self):
        test_obj = TestModelCreator()
        result = test_obj.create_random_username()
        self.assertTrue(result, str)
        self.assertEqual(len(result), 10)

    def test_create_randomnumber(self):
        test_obj = TestModelCreator()
        result = test_obj.create_randnumber()
        self.assertIs(type(result), int)

    def test_create_random_inn(self):
        test_obj = TestModelCreator()
        result = test_obj.create_random_inn()
        self.assertTrue(result, str)
        self.assertEqual(len(result), 10)

    def test_create_docs_contract(self):
        test_obj = TestModelCreator()
        result = test_obj.create_docs_contract()
        self.assertTrue(result, DocumentsContractEggsModel)

    def test_create_deal_docs(self):
        test_obj = TestModelCreator()
        result = test_obj.create_deal_docs()
        self.assertTrue(result, DocumentsDealEggsModel)

    def test_create_tail(self):
        test_obj = TestModelCreator()
        result = test_obj.create_tail()
        self.assertTrue(result, TailsContragentModelEggs)

    def test_create_user_manager(self):
        test_obj = TestModelCreator()
        result = test_obj.create_user('manager')
        self.assertTrue(result, CustomUser)
        if isinstance(result, CustomUser):
            self.assertEqual(result.role, '2')

    def test_create_user_logic(self):
        test_obj = TestModelCreator()
        result = test_obj.create_user('logic')
        self.assertTrue(result, CustomUser)
        if isinstance(result, CustomUser):
            self.assertEqual(result.role, '4')

    def test_create_user_napr(self):
        test_obj = TestModelCreator()
        result = test_obj.create_user('napr')
        self.assertTrue(result, CustomUser)
        if isinstance(result, CustomUser):
            self.assertEqual(result.role, '5')

    def test_create_user_fin(self):
        test_obj = TestModelCreator()
        result = test_obj.create_user('fin')
        self.assertTrue(result, CustomUser)
        if isinstance(result, CustomUser):
            self.assertEqual(result.role, '6')

    def test_create_user_buh(self):
        test_obj = TestModelCreator()
        result = test_obj.create_user('buh')
        self.assertTrue(result, CustomUser)
        if isinstance(result, CustomUser):
            self.assertEqual(result.role, '7')

    def test_create_additional_exp(self):
        test_obj = TestModelCreator()
        result = test_obj.create_additional_exp()
        self.assertTrue(result, AdditionalExpenseEggs)

    def test_create_comment_json(self):
        test_obj = TestModelCreator()
        result = test_obj.create_comment_json()
        self.assertTrue(result, CommentEggs)

    def test_create_seller(self):
        test_obj = TestModelCreator()
        result = test_obj.create_seller()
        self.assertTrue(result, SellerCardEggs)

    def test_create_buyer(self):
        test_obj = TestModelCreator()
        result = test_obj.create_buyer()
        self.assertTrue(result, BuyerCardEggs)

    def test_create_logic(self):
        test_obj = TestModelCreator()
        result = test_obj.create_logic()
        self.assertTrue(result, LogicCardEggs)

    def test_create_app_seller(self):
        test_obj = TestModelCreator()
        result = test_obj.create_app_seller()
        self.assertTrue(result, ApplicationFromSellerBaseEggs)

    def test_create_app_buyer(self):
        test_obj = TestModelCreator()
        result = test_obj.create_app_buyer()
        self.assertTrue(result, ApplicationFromBuyerBaseEggs)

    def test_create_base_deal(self):
        test_obj = TestModelCreator()
        result = test_obj.create_base_deal()
        self.assertTrue(result, BaseDealEggsModel)










