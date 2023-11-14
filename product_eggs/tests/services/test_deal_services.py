from django.test import TestCase
from rest_framework import serializers

from product_eggs.services.base_deal.deal_services import status_check
from product_eggs.tests.create_models import TestModelCreator


class TestDealServices(TestCase):

    def test_status_check(self):
        test_obj = TestModelCreator()
        deal = test_obj.create_base_deal()
        deal.status = 3
        self.assertEqual(status_check(deal, [3 ,4]), None)
        deal.status = 1
        status = [3, 4]
        self.assertRaises(serializers.ValidationError, status_check, deal, status)
