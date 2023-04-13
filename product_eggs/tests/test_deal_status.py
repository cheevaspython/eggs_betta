from django.test import TestCase
from rest_framework import exceptions

from product_eggs.services.deal_status import change_status_deal, check_processing_to_confirm, get_message_and_user
from product_eggs.services.message_send_save import search_done_deal_messages_and_turn_off_fields_is_value, \
        search_done_calc_and_conf_calc_messages_and_turn_off_fields_is_value
from product_eggs.models.calcs_deal_eggs import DealEggs, ConfirmedCalculateEggs, CalculateEggs
from product_eggs.models.apps_eggs import ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs, LogicCardEggs, RequisitesEggs
from users.models import CustomUser


def create_data_base():
    test_requisites1 = RequisitesEggs.objects.create(general_manager='test1') 
    test_requisites2 = RequisitesEggs.objects.create(general_manager='test2') 
    test_requisites3 = RequisitesEggs.objects.create(general_manager='test3') 
    test_user_manager_s = CustomUser.objects.create(username='tester_s', role=1)
    test_user_manager_b = CustomUser.objects.create(username='tester_b', role=2)
    test_user_manager1 = CustomUser.objects.create(username='tester1', role=6)
    test_user_manager2 = CustomUser.objects.create(username='tester2', role=7)
    test_buyer = BuyerCardEggs.objects.create(name='test_buyer', requisites=test_requisites1)
    test_seller = SellerCardEggs.objects.create(name='test_seller', requisites=test_requisites2)
    test_logic = LogicCardEggs.objects.create(name='test_logic', requisites=test_requisites3)
    test_app_buyer = ApplicationFromBuyerBaseEggs.objects.create(owner=test_user_manager_b, current_buyer=test_buyer)
    test_app_seller = ApplicationFromSellerBaseEggs.objects.create(owner=test_user_manager_s, c0=100, c0_cost=10, c1=80, c1_cost=50, \
        c2=40, c2_cost=50, c3=10, c3_cost=90, dirt=0, dirt_cost=0, current_seller=test_seller)
    test_calc = CalculateEggs.objects.create(application_from_buyer=test_app_buyer, \
        application_from_seller=test_app_seller, average_delivery_cost=100)
    test_conf_calc = ConfirmedCalculateEggs.objects.create(current_calculate=test_calc, current_logic=test_logic)
    test_object = DealEggs.objects.create(confirmed_calculate=test_conf_calc, status=1, processing_to_confirm=False)
    return test_object, test_user_manager1, test_user_manager2, test_user_manager_b, test_user_manager_s


class ChangeStatusDealTestCase(TestCase):

    def test_status_change(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        change_status_deal(test_object)

        self.assertEqual(test_object.status, 2)

    def test_processing_to_confirm(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        change_status_deal(test_object)

        self.assertEqual(test_object.processing_to_confirm, True)

    def test_check_processing_to_confirm_true(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        check_processing_to_confirm(test_object)      

        self.assertEqual(test_object.processing_to_confirm, True)
        self.assertEqual(test_object.status, 2)
    
    def test_check_processing_to_confirm_False(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.processing_to_confirm = True
        check_processing_to_confirm(test_object)      
         
        self.assertEqual(test_object.processing_to_confirm, True)
        self.assertEqual(test_object.status, 1)

    def test_get_message_and_user_status1(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_message_and_owner = get_message_and_user(test_object)

        self.assertEqual(test_message_and_owner.message, f'Сделка №{test_object.pk} ожидает подтверждения') 
        self.assertEqual(test_message_and_owner.owner, test_usr6 )

    def test_get_message_and_user_status2(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.status = 2
        test_message_and_owner = get_message_and_user(test_object)

        self.assertEqual(test_message_and_owner.message, f'Загрузите документы, основание для платежа, по сделке №{test_object.pk}') 
        self.assertEqual(test_message_and_owner.owner, test_usr_s)

    def test_get_message_and_user_status3(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.status = 3
        test_message_and_owner = get_message_and_user(test_object)

        self.assertEqual(test_message_and_owner.message, f'Подтвердите оплату по сделке №{test_object.pk}') 
        self.assertEqual(test_message_and_owner.owner, test_usr6)

    def test_get_message_and_user_status4(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.status = 4
        test_message_and_owner = get_message_and_user(test_object)

        self.assertEqual(test_message_and_owner.message, f'Оплатите счет по сделке №{test_object.pk} и загрузите его')
        self.assertEqual(test_message_and_owner.owner, test_usr7)

    def test_get_message_and_user_status5(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.status = 5
        test_message_and_owner = get_message_and_user(test_object)

        self.assertEqual(test_message_and_owner.message, f'Счет по сделке №{test_object.pk} оплачен, проконтролируйте погрузку и загрузите УПД')
        self.assertEqual(test_message_and_owner.owner, test_usr_s)
    
    def test_get_message_and_user_status6(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.status = 6
        test_message_and_owner = get_message_and_user(test_object)

        self.assertEqual(test_message_and_owner.message, f'По сделке №{test_object.pk} товар в пути, ожидаем от вас запрос исходящей УПД')
        self.assertEqual(test_message_and_owner.owner, test_usr_b)
    
    def test_get_message_and_user_status7(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.status = 7
        test_message_and_owner = get_message_and_user(test_object)

        self.assertEqual(test_message_and_owner.message, f'По сделке №{test_object.pk} загрузите исходящую УПД')
        self.assertEqual(test_message_and_owner.owner, test_usr7)

    def test_get_message_and_user_status8(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.status = 8
        test_message_and_owner = get_message_and_user(test_object)

        self.assertEqual(test_message_and_owner.message, f'Проконтролируйте разгрузку по сделке №{test_object.pk}, загрузите подписанную УПД')
        self.assertEqual(test_message_and_owner.owner, test_usr_b)

    def test_get_message_and_user_status9(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.status = 9
        test_message_and_owner = get_message_and_user(test_object)

        self.assertEqual(test_message_and_owner.message, f'Сделка №{test_object.pk} закрыта')
        self.assertEqual(test_message_and_owner.owner, test_usr6)
    
    def test_get_message_and_user_status10(self):
        test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
        test_object.status = 10
        self.assertRaises(exceptions.ValidationError, get_message_and_user, \
                test_object)


# class SearchDealCalcsIDTestCase(TestCase):
#     
#     def test_search_deal(self):
#         test_object, test_usr6, test_usr7, test_usr_b, test_usr_s = create_data_base()
#         search_done_deal_messages_and_turn_off_fields_is_value(test_object)
#
#     def test_search_calcs(self):
#         test_conf_calc, test_logic = create_conf_calc_and_logic()
#         search_done_calc_and_conf_calc_messages_and_turn_off_fields_is_value(test_conf_calc)






