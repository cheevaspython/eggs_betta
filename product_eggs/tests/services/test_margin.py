from django.test import TestCase

from product_eggs.services.base_deal.margin import calculate_margin
from product_eggs.tests.create_models import TestModelCreator


class MarginTestCase(TestCase):

    def test_calc_margin_default(self):
        test_obj = TestModelCreator()
        deal = test_obj.create_base_deal()
        deal.status = 3
        result = calculate_margin(deal)
        self.assertEqual(result, 355515.08)

    def test_calc_margin_1(self):
        test_obj = TestModelCreator()
        deal = test_obj.create_base_deal()
        deal.status = 3
        deal.delivery_cost = 1000
        deal.cB_white = 360
        deal.cB_cream = 0
        deal.cB_brown = 0
        deal.c0_white = 0
        deal.c0_cream = 0
        deal.c0_brown = 0
        deal.c1_white = 0
        deal.c1_cream = 0
        deal.c1_brown = 0
        deal.c2_white = 0
        deal.c2_cream = 0
        deal.c2_brown = 0
        deal.c3_white = 0
        deal.c3_cream = 0
        deal.c3_brown = 0
        deal.dirt = 0
        deal.seller_cB_white_cost = 10
        deal.seller_cB_cream_cost = 0
        deal.seller_cB_brown_cost = 0
        deal.seller_c0_white_cost = 0
        deal.seller_c0_cream_cost = 0
        deal.seller_c0_brown_cost = 0
        deal.seller_c1_white_cost = 0
        deal.seller_c1_cream_cost = 0
        deal.seller_c1_brown_cost = 0
        deal.seller_c2_white_cost = 0
        deal.seller_c2_cream_cost = 0
        deal.seller_c2_brown_cost = 0
        deal.seller_c3_white_cost = 0
        deal.seller_c3_cream_cost = 0
        deal.seller_c3_brown_cost = 0
        deal.seller_dirt_cost = 0
        deal.buyer_cB_white_cost = 20
        deal.buyer_cB_cream_cost = 0
        deal.buyer_cB_brown_cost = 0
        deal.buyer_c0_white_cost = 0
        deal.buyer_c0_cream_cost = 0
        deal.buyer_c0_brown_cost = 0
        deal.buyer_c1_white_cost = 0
        deal.buyer_c1_cream_cost = 0
        deal.buyer_c1_brown_cost = 0
        deal.buyer_c2_white_cost = 0
        deal.buyer_c2_cream_cost = 0
        deal.buyer_c2_brown_cost = 0
        deal.buyer_c3_white_cost = 0
        deal.buyer_c3_cream_cost = 0
        deal.buyer_c3_brown_cost = 0
        deal.buyer_dirt_cost = 0
        result = calculate_margin(deal)
        self.assertEqual(result, 2278.78)
