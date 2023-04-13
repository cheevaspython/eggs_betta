from django.test import TestCase

from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs, RequisitesEggs
from product_eggs.serializers.base_card_serializers import BuyerCardEggsDetailSerializer, \
        SellerCardEggsDetailSerializer, RequisitesDetailSerializer


class BuyerCardSerializerTestCase(TestCase):
    def test_buyercardeggs(self):
        buyer_card_1 = BuyerCardEggs.objects.create(name='test buyer 1', inn='109238')
        buyer_card_2 = BuyerCardEggs.objects.create(name='test buyer 2', inn='109239')
        data = BuyerCardEggsDetailSerializer([buyer_card_1, buyer_card_2], many=True).data
        expected_data = [
                {
                    'id': buyer_card_1.id,
                    'name': 'test buyer 1',
                    'inn': '109238',
                    'contact_person': None,
                    'phone': None, 
                    'email': None, 
                    'pay_type': None, 
                    'comment': None, 
                    'requisites': None, 
                    'current_requisites': None,
                    'warehouse_address_1': None, 
                    'warehouse_address_2': None, 
                    'warehouse_address_3': None, 
                    'warehouse_address_4': None, 
                    'warehouse_address_5': None,
                },
                {
                    'id': buyer_card_2.id,
                    'name': 'test buyer 2',
                    'inn': '109239',
                    'contact_person': None,
                    'phone': None, 
                    'email': None, 
                    'pay_type': None, 
                    'comment': None, 
                    'requisites': None, 
                    'current_requisites': None,
                    'warehouse_address_1': None, 
                    'warehouse_address_2': None, 
                    'warehouse_address_3': None, 
                    'warehouse_address_4': None, 
                    'warehouse_address_5': None,
                },
            ]
        self.assertEqual(expected_data, data)


class SellerCardSerializerTestCase(TestCase):
    def test_sellercardeggs(self):
        seller_card_1 = SellerCardEggs.objects.create(name='test seller 1', inn='109238', contact_person='TestA', \
                phone='123456', email='a@a.com', pay_type=None, comment='test_comment', requisites=None, \
                prod_address_1='test_addr', prod_address_2='test_addr2')
        seller_card_2 = SellerCardEggs.objects.create(name='test seller 2', inn='109239', contact_person='TestB', \
                phone='1234567', email='a1@a.com', pay_type=None, comment='test_comment', requisites=None, \
                prod_address_1='test_addr1', prod_address_2='test_addr12')
        data = SellerCardEggsDetailSerializer([seller_card_1, seller_card_2], many=True).data
        expected_data = [
                {
                    'id': seller_card_1.id,
                    'name': 'test seller 1',
                    'inn': '109238',
                    'contact_person': 'TestA',
                    'phone': '123456', 
                    'email': 'a@a.com', 
                    'pay_type': None, 
                    'comment': 'test_comment', 
                    'requisites': None, 
                    'current_requisites': None,
                    'prod_address_1': 'test_addr', 
                    'prod_address_2': 'test_addr2', 
                    'prod_address_3': None, 
                    'prod_address_4': None, 
                    'prod_address_5': None,
                },
                {
                    'id': seller_card_2.id,
                    'name': 'test seller 2',
                    'inn': '109239',
                    'contact_person': 'TestB',
                    'phone': '1234567', 
                    'email': 'a1@a.com', 
                    'pay_type': None, 
                    'comment': 'test_comment', 
                    'requisites': None, 
                    'current_requisites': None,
                    'prod_address_1': 'test_addr1', 
                    'prod_address_2': 'test_addr12', 
                    'prod_address_3': None, 
                    'prod_address_4': None, 
                    'prod_address_5': None,
                },
            ]
        self.assertEqual(expected_data, data)


class RequisitesTestCase(TestCase):

    def test_requisites(self):
        test_requisites = RequisitesEggs.objects.create(
                general_manager='A B C', inn='1234567890', bank_name='test', bic_bank='1234', 
                cor_account='31019823', customers_pay_account='431029348092384', legal_address='test1',
                physical_address='test2' 
        )
        requisites_data = RequisitesDetailSerializer(test_requisites).data
        expected_data_requisites = [
                            {
                        'id': test_requisites.id,
                        'general_manager': 'A B C',
                        'inn': '1234567890',
                        'bank_name': 'test', 
                        'bic_bank': '1234', 
                        'cor_account': '31019823', 
                        'customers_pay_account': '431029348092384',
                        'legal_address':'test1',
                        'physical_address': 'test2' 
                            },
                        ] 

        self.assertEqual(expected_data_requisites[0], requisites_data)







