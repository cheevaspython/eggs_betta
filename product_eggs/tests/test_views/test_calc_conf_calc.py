# from django.test import TestCase
# from rest_framework.test import APITestCase
#
# from product_eggs.views.calc_views import CalculateEggs, ConfirmedCalculateEggs
# from product_eggs.models.calcs_deal_eggs import DealEggs, ConfirmedCalculateEggs, CalculateEggs
# from product_eggs.models.apps_eggs import ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
# from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs, LogicCardEggs, RequisitesEggs
# from users.models import CustomUser
#
# def create_calc_conf_calc():
#         test_requisites1 = RequisitesEggs.objects.create(general_manager='test1') 
#         test_requisites2 = RequisitesEggs.objects.create(general_manager='test2') 
#         test_requisites3 = RequisitesEggs.objects.create(general_manager='test3') 
#         test_user_manager_s = CustomUser.objects.create(username='tester_s', role=1)
#         test_user_manager_b = CustomUser.objects.create(username='tester_b', role=2)
#         test_user_manager1 = CustomUser.objects.create(username='tester1', role=6)
#         test_user_manager2 = CustomUser.objects.create(username='tester2', role=7)
#         test_buyer = BuyerCardEggs.objects.create(name='test_buyer', requisites=test_requisites1)
#         test_seller = SellerCardEggs.objects.create(name='test_seller', requisites=test_requisites2)
#         test_logic = LogicCardEggs.objects.create(name='test_logic', requisites=test_requisites3)
#         test_app_buyer = ApplicationFromBuyerBaseEggs.objects.create(owner=test_user_manager_b, current_buyer=test_buyer)
#         test_app_seller = ApplicationFromSellerBaseEggs.objects.create(owner=test_user_manager_s, c0=100, c0_cost=10, c1=80, c1_cost=50, \
#             c2=40, c2_cost=50, c3=10, c3_cost=90, dirt=0, dirt_cost=0, current_seller=test_seller)
#         test_calc = CalculateEggs.objects.create(application_from_buyer=test_app_buyer, \
#             application_from_seller=test_app_seller, average_delivery_cost=100)
#         test_conf_calc = ConfirmedCalculateEggs.objects.create(current_calculate=test_calc, current_logic=test_logic)
#         test_deal = DealEggs.objects.create(confirmed_calculate=test_conf_calc, status=1, processing_to_confirm=False)
#         return test_calc, test_conf_calc
#
# class CalcCardEggsTestCase(APITestCase):
#
#     def test_perform_update(self, serializer):
#         test_calc, test_conf_calc = create_data_base()
#         # serializer.save()
#         # obj = self.queryset.get(id=serializer.data['id'])
#         #
#         # if obj.calc_ready:
#         #     check_fields_values_to_calc_ready(obj)
#         #     message = f'Одобрите подтвержденный просчет №{obj.pk} для перехода в статус Сделка.'
#         #     owner = CustomUser.objects.get(role=5)
#         #     create_send_and_save_message(message, owner, conf_calculate=obj)
#
#
#     def test_get(self):
#         buyer_card_1 = BuyerCardEggs.objects.create(name='test buyer 1', inn='109238')
#         buyer_card_2 = BuyerCardEggs.objects.create(name='test buyer 2', inn='109239')
#         url = 'http://127.0.0.1:8000/api/eggs/buyer_card/'
#         response = self.client.get(url)
#         serializer_data = BuyerCardEggsDetailSerializer([buyer_card_1, buyer_card_2], many=True).data
#         self.assertEqual(status.HTTP_200_OK, response.status_code)
#         self.assertEqual(serializer_data, response.data)
#
#
#
#                 
