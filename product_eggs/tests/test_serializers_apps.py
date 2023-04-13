from django.test import TestCase

from product_eggs.serializers.apps_serializers_eggs import ApplicationBuyerEggsDetailSerializer, \
        ApplicationSellerEggsDetailSerializer
from product_eggs.models.apps_eggs import ApplicationFromSellerBaseEggs, ApplicationFromBuyerBaseEggs
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs, RequisitesEggs
from users.models import CustomUser



class ApplicationFromBuyerBaseEggsTestCase(TestCase):
    
    def test_application_buyer_one_model(self):
        test_buyer = BuyerCardEggs.objects.create(name='test buyer', inn='109238')
        test_user = CustomUser.objects.create(username='tester_b', role=2)
        buyer_application = ApplicationFromBuyerBaseEggs.objects.create(
                owner=test_user, delivery_window_from='2022-12-12', delivery_window_until='2022-10-10',
                c0=100, c0_cost=250, c2=80, c2_cost=200, current_buyer=test_buyer, unloading_address='1 test street',
                comment='test comment',
                )
        data = ApplicationBuyerEggsDetailSerializer(buyer_application).data 
        expected_data = [{
                    'id': buyer_application.id,
                    'owner': test_user.id,
                    'delivery_window_from': '2022-12-12',
                    'delivery_window_until': '2022-10-10',
                    'c0': 100,
                    'c0_cost': 250,
                    'c1': None,
                    'c1_cost': None,
                    'c2': 80,
                    'c2_cost': 200,
                    'c3': None,
                    'c3_cost': None,
                    'dirt': None,
                    'dirt_cost': None,
                    'current_buyer': test_buyer.id,
                    'buyer_card_detail': [
                        {
                            'id': test_buyer.id,       #TODO sdelat otdelno, potom vstavit
                            'name': 'test buyer', 
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
                        ],
                    'unloading_address': '1 test street',
                    'comment': 'test comment',
                    'owner_detail': [
                        {
                            'id': test_user.id,
                            'username': 'tester_b',
                            'role': '2',
                            'first_name': None,
                            'last_name': None,
                            'email': None,
                            },
                        ],
                    },
                ]
        self.assertEqual(data, expected_data)
