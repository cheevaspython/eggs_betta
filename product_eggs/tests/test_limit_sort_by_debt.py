from django.test import TestCase

from product_eggs.models.calcs_deal_eggs import DealEggs, ConfirmedCalculateEggs, CalculateEggs
from product_eggs.models.apps_eggs import ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs, LogicCardEggs, RequisitesEggs
from users.models import CustomUser
from product_eggs.serializers.limit_buyers_eggs import DutyBuyersSerializer
from product_eggs.services.limit_sort_by_debt import sort_by_debt_and_hide_zero_count, add_debt_to_buyer, \
    summ_debt_in_current_application_from_buyer_card


def create_data_base():
    test_requisites1 = RequisitesEggs.objects.create(general_manager='test1') 
    test_requisites2 = RequisitesEggs.objects.create(general_manager='test2') 
    test_requisites3 = RequisitesEggs.objects.create(general_manager='test3') 
    test_user_manager_s = CustomUser.objects.create(username='tester_s', role=1)
    test_user_manager_b = CustomUser.objects.create(username='tester_b', role=2)
    test_user_manager1 = CustomUser.objects.create(username='tester1', role=6)
    test_user_manager2 = CustomUser.objects.create(username='tester2', role=7)
    test_buyer = BuyerCardEggs.objects.create(name='test_buyer', requisites=test_requisites1, \
            current_debt=1900, pay_limit=22000)
    test_seller = SellerCardEggs.objects.create(name='test_seller', requisites=test_requisites2)
    test_logic = LogicCardEggs.objects.create(name='test_logic', requisites=test_requisites3)
    test_app_buyer = ApplicationFromBuyerBaseEggs.objects.create(owner=test_user_manager_b, current_buyer=test_buyer)
    test_app_seller = ApplicationFromSellerBaseEggs.objects.create(owner=test_user_manager_s, c0=100, c0_cost=50, c1=80, c1_cost=40, \
        c2=0, c2_cost=0, c3=10, c3_cost=20, dirt=0, dirt_cost=0, current_seller=test_seller)
    test_calc = CalculateEggs.objects.create(application_from_buyer=test_app_buyer, \
        application_from_seller=test_app_seller, average_delivery_cost=100)
    test_conf_calc = ConfirmedCalculateEggs.objects.create(current_calculate=test_calc, current_logic=test_logic)
    test_object = DealEggs.objects.create(confirmed_calculate=test_conf_calc, status=1, processing_to_confirm=False)
    return test_object


class SortbyDebtHideZeroCountTestCase(TestCase):

    def test_sort_debt(self):
        test_requisites1 = RequisitesEggs.objects.create(general_manager='test1') 
        test_requisites2 = RequisitesEggs.objects.create(general_manager='test2') 
        test_requisites3 = RequisitesEggs.objects.create(general_manager='test3') 
        test_buyer = BuyerCardEggs.objects.create(name='test_buyer', requisites=test_requisites1, \
            current_debt=1900, pay_limit=22000)
        test_buyer1 = BuyerCardEggs.objects.create(name='test_buyer1', requisites=test_requisites2, \
            current_debt=12992, pay_limit=15000)
        test_buyer2 = BuyerCardEggs.objects.create(name='test_buyer2', requisites=test_requisites3, \
            current_debt=0, pay_limit=2200)
        data1 = DutyBuyersSerializer(test_buyer)
        data2 = DutyBuyersSerializer(test_buyer1)
        all_buyers = BuyerCardEggs.objects.all()
        serialize_test = DutyBuyersSerializer(all_buyers, many=True) 
        result = sort_by_debt_and_hide_zero_count(serialize_test.data) 
        response_data = [data2.data, data1.data]
        self.assertEqual(result, response_data)

    def test_add_debt_to_buyer(self):
        test_deal = create_data_base() 
        add_debt_to_buyer(test_deal)
        self.assertEqual(test_deal.confirmed_calculate.current_calculate.application_from_buyer.current_buyer.current_debt, 10300)

    def test_summ_debt_in_current_application_from_buyer_card(self):
        test = create_data_base()
        test.confirmed_calculate.current_calculate.application_from_seller.c0 = 192.80 
        test.confirmed_calculate.current_calculate.application_from_seller.c0_cost = 13 
        test.confirmed_calculate.current_calculate.application_from_seller.c1 = 0 
        test.confirmed_calculate.current_calculate.application_from_seller.c1_cost = 300 
        test.confirmed_calculate.current_calculate.application_from_seller.c2 = 79.3 
        test.confirmed_calculate.current_calculate.application_from_seller.c2_cost = 0 
        test.confirmed_calculate.current_calculate.application_from_seller.c3 = 480 
        test.confirmed_calculate.current_calculate.application_from_seller.c3_cost = 12.390 
        test.confirmed_calculate.current_calculate.application_from_seller.dirt = 890
        test.confirmed_calculate.current_calculate.application_from_seller.dirt_cost = 1.5 
        result = summ_debt_in_current_application_from_buyer_card(test)
        self.assertEqual(2506.4 + 0 + 0 + 5947.2 + 1335, result)

        

