from django.test import TestCase

from rest_framework import serializers
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.messages import MessageToUserEggs

from product_eggs.tests.create_models import TestModelCreator
from product_eggs.services.base_deal.deal_status_change import DealStatusChanger


class TestDealStatusChanger(TestCase):

    def create_test_deal(self):
        test_obj = TestModelCreator()
        self.deal = test_obj.create_base_deal(3)
        self.manager = test_obj.create_user('manager')
        self.logic = test_obj.create_user('logic')
        self.napr = test_obj.create_user('napr')
        self.fin = test_obj.create_user('fin')
        self.buh = test_obj.create_user('buh')

    def test_init(self):
        self.create_test_deal()
        self.deal.status = 2
        self.assertRaises(serializers.ValidationError, DealStatusChanger, self.deal, self.manager)
        self.deal.status = 3
        deal_changer = DealStatusChanger(self.deal, self.manager)
        self.assertEqual(deal_changer.user, self.manager)
        self.assertEqual(deal_changer.instance, self.deal)

    def test_main(self):
        self.create_test_deal()
        self.deal.deal_status = 0
        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.manager)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.get(message_to=self.fin.pk)
        self.assertTrue(mes)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 1)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.manager)
        self.assertRaises(serializers.ValidationError, deal_changer.status_changer_main)
        deal_changer = DealStatusChanger(self.deal, self.fin)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.get(message_to=self.deal.application_from_seller.owner)
        self.assertTrue(mes)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 2)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.deal.seller.manager)
        self.assertRaises(serializers.ValidationError, deal_changer.status_changer_main)
        deal_changer = DealStatusChanger(self.deal, self.deal.application_from_seller.owner)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.filter(message_to=self.fin.pk)
        self.assertTrue(mes)
        self.assertEqual(len(mes), 2)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 3)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.fin)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.filter(message_to=self.buh.pk)
        self.assertTrue(mes)
        self.assertEqual(len(mes), 1)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 4)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.buh)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.filter(message_to=self.deal.application_from_seller.owner)
        self.assertTrue(mes)
        self.assertEqual(len(mes), 2)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 5)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.deal.application_from_seller.owner)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.filter(message_to=self.deal.application_from_buyer.owner)
        self.assertTrue(mes)
        self.assertEqual(len(mes), 1)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 6)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.deal.application_from_buyer.owner)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.filter(message_to=self.buh)
        self.assertTrue(mes)
        self.assertEqual(len(mes), 2)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 7)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.buh)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.filter(message_to=self.deal.application_from_buyer.owner)
        self.assertTrue(mes)
        self.assertEqual(len(mes), 2)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 8)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.deal.application_from_buyer.owner)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.filter(message_to=self.buh)
        self.assertTrue(mes)
        self.assertEqual(len(mes), 3)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 9)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.buh)
        deal_changer.status_changer_main()
        mes_fin = MessageToUserEggs.objects.filter(message_to=self.fin)
        mes_sel = MessageToUserEggs.objects.filter(message_to=self.deal.application_from_seller.owner)
        mes_buy = MessageToUserEggs.objects.filter(message_to=self.deal.application_from_buyer.owner)
        self.assertEqual(len(mes_sel), 4)
        self.assertEqual(len(mes_fin), 3)
        self.assertEqual(len(mes_buy), 4)
        self.assertTrue(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 10)
        self.assertEqual(self.deal.status, 4)

    def test_main_edo(self):
        self.create_test_deal()
        self.deal.deal_status = 4
        self.deal.documents.edo_seller_documents = True
        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.buh)
        deal_changer.status_changer_main()
        mes = MessageToUserEggs.objects.filter(message_to=self.deal.application_from_seller.owner)
        mes_buh = MessageToUserEggs.objects.filter(message_to=self.buh)
        self.assertTrue(mes)
        self.assertTrue(mes_buh)
        self.assertEqual(len(mes), 1)
        self.assertEqual(len(mes_buh), 1)
        self.assertTrue(self.deal.deal_status_multi)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertEqual(self.deal.deal_status, 5)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.buh)
        deal_changer.status_changer_main()
        self.assertEqual(self.deal.deal_status, 5)
        self.assertFalse(self.deal.deal_status_ready_to_change)
        self.assertFalse(self.deal.deal_status_multi)

        self.deal.deal_status_ready_to_change = True
        deal_changer = DealStatusChanger(self.deal, self.deal.application_from_seller.owner)
        deal_changer.status_changer_main()
        self.assertFalse(self.deal.deal_status_multi)
        self.assertEqual(self.deal.deal_status, 6)
        self.assertFalse(self.deal.deal_status_ready_to_change)






