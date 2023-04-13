from django.test import TestCase
from rest_framework import exceptions

from product_eggs.services.check_calc_ready import check_fields_values_to_calc_ready, turn_off_fields_is_active
from product_eggs.services.message_send_save import search_done_deal_messages_and_turn_off_fields_is_value, \
        search_done_calc_and_conf_calc_messages_and_turn_off_fields_is_value
from product_eggs.models.calcs_deal_eggs import ConfirmedCalculateEggs, CalculateEggs
from product_eggs.models.apps_eggs import ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs, LogicCardEggs, RequisitesEggs
from product_eggs.models.message_to_user_eggs import MessageToUserEggs
from product_eggs.tests.test_deal_status import create_data_base as deal_data_base
from users.models import CustomUser


def create_data_base():
    test_requisites1 = RequisitesEggs.objects.create(general_manager='test1') 
    test_requisites2 = RequisitesEggs.objects.create(general_manager='test2') 
    test_requisites3 = RequisitesEggs.objects.create(general_manager='test3') 
    test_user_manager_s = CustomUser.objects.create(username='tester_s', role=1)
    test_user_manager_b = CustomUser.objects.create(username='tester_b', role=2)
    test_buyer = BuyerCardEggs.objects.create(name='test_buyer', requisites=test_requisites1)
    test_seller = SellerCardEggs.objects.create(name='test_seller', requisites=test_requisites2)
    test_logic = LogicCardEggs.objects.create(name='test_logic', requisites=test_requisites3)
    test_app_buyer = ApplicationFromBuyerBaseEggs.objects.create(owner=test_user_manager_b, current_buyer=test_buyer)
    test_app_seller = ApplicationFromSellerBaseEggs.objects.create(owner=test_user_manager_s, c0=100, c0_cost=10, c1=80, c1_cost=50, \
        c2=40, c2_cost=50, c3=10, c3_cost=90, dirt=0, dirt_cost=0, current_seller=test_seller)
    test_calc = CalculateEggs.objects.create(application_from_buyer=test_app_buyer, \
        application_from_seller=test_app_seller, average_delivery_cost=100)
    test_conf_calc = ConfirmedCalculateEggs.objects.create(current_calculate=test_calc)
    return test_conf_calc, test_logic


class CalcReadyTestCase(TestCase):
    
    def test_check_fields_calc_ready_only_ready(self):
        test_conf_calc, test_logic  = create_data_base()
        test_conf_calc.calc_is_ready = True
        self.assertRaises(exceptions.ValidationError, check_fields_values_to_calc_ready, \
                test_conf_calc)
        self.assertEqual(test_conf_calc.calc_ready, False)
    
    def test_check_fields_calc_ready_only_logic(self):
        test_conf_calc, test_logic  = create_data_base()
        test_conf_calc.calc_is_ready = True
        test_conf_calc.current_logic = test_logic
        self.assertRaises(exceptions.ValidationError, check_fields_values_to_calc_ready, \
                test_conf_calc)
        self.assertEqual(test_conf_calc.calc_ready, False)
    
    def test_check_fields_calc_ready_logic_and_delivery_date_from_seller(self):
        test_conf_calc, test_logic  = create_data_base()
        test_conf_calc.calc_is_ready = True
        test_conf_calc.current_logic = test_logic
        test_conf_calc.delivery_date_from_seller = '2023-10-10'
        self.assertRaises(exceptions.ValidationError, check_fields_values_to_calc_ready, \
                test_conf_calc)
        self.assertEqual(test_conf_calc.calc_ready, False)

    def test_check_fields_calc_ready_logic_and_delivery_date_from_seller_buyer(self):
        test_conf_calc, test_logic  = create_data_base()
        test_conf_calc.calc_is_ready = True
        test_conf_calc.current_logic = test_logic
        test_conf_calc.delivery_date_from_seller = '2023-10-10'
        test_conf_calc.delivery_date_to_buyer = '2023-10-11'
        self.assertRaises(exceptions.ValidationError, check_fields_values_to_calc_ready, \
                test_conf_calc)
        self.assertEqual(test_conf_calc.calc_ready, False)

    def test_check_fields_calc_ready_full_fields(self):
        test_conf_calc, test_logic  = create_data_base()
        test_conf_calc.current_logic = test_logic
        test_conf_calc.delivery_date_from_seller = '2023-10-10'
        test_conf_calc.delivery_date_to_buyer = '2023-10-11'
        test_conf_calc.delivery_cost = 1201
        test_conf_calc.calc_is_ready = True
        self.assertEqual(check_fields_values_to_calc_ready(test_conf_calc), None)


class TurnOffFieldsIsActiveTestCase(TestCase):
    
    def test_turn_off_one_model(self):
        test_conf_calc, test_logic = create_data_base()
        test_conf_calc.is_active = True
        turn_off_fields_is_active(test_conf_calc)
        self.assertEqual(test_conf_calc.is_active, False)

    def test_turn_off_tree_models(self):
        test_conf_calc1, test_logic = create_data_base()
        test_conf_calc1.is_active = True
        test_requisites1a = RequisitesEggs.objects.create(general_manager='test1a') 
        test_requisites2a = RequisitesEggs.objects.create(general_manager='test2a') 
        test_requisites3a = RequisitesEggs.objects.create(general_manager='test3a') 
        test_user_manager_s1 = CustomUser.objects.create(username='tester_s1', role=1)
        test_user_manager_b1 = CustomUser.objects.create(username='tester_b2', role=2)
        test_buyer1 = BuyerCardEggs.objects.create(name='test_buyer1', requisites=test_requisites1a)
        test_seller1 = SellerCardEggs.objects.create(name='test_seller1', requisites=test_requisites2a)
        test_logic1 = LogicCardEggs.objects.create(name='test_logic1', requisites=test_requisites3a)
        test_app_buyer1 = ApplicationFromBuyerBaseEggs.objects.create(owner=test_user_manager_b1, current_buyer=test_buyer1)
        test_app_seller1 = ApplicationFromSellerBaseEggs.objects.create(owner=test_user_manager_s1, c0=100, c0_cost=10, c1=80, c1_cost=50, \
            c2=40, c2_cost=50, c3=10, c3_cost=90, dirt=0, dirt_cost=0, current_seller=test_seller1)
        test_calc = CalculateEggs.objects.create(application_from_buyer=test_app_buyer1, \
            application_from_seller=test_app_seller1, average_delivery_cost=100)
        test_conf_calc = ConfirmedCalculateEggs.objects.create(current_calculate=test_calc, current_logic=test_logic1, \
                is_active=True)
        turn_off_fields_is_active((test_conf_calc, test_conf_calc1, test_calc,))
        self.assertEqual(test_conf_calc1.is_active, False)
        self.assertEqual(test_conf_calc.is_active, False)
        self.assertEqual(test_calc.is_active, False)

    def test_turn_off_message_field(self):
        test_conf_calc1, test_logic = create_data_base()
        test_user_manager_s1 = CustomUser.objects.create(username='tester_s1', role=1)
        message = 'test message'
        message_to = MessageToUserEggs.objects.create(notification_to=test_user_manager_s1, current_conf_calculate=test_conf_calc1, \
                notification_message=message)
        turn_off_fields_is_active(message_to)
        self.assertEqual(message_to.is_active, False)


class SearchDoneDealMessages(TestCase):
    
    def test_search_done_deal_messages(self):
        test_object, test_user_manager1, test_user_manager2, test_user_manager_b, test_user_manager_s = deal_data_base()
        message = 'test message'
        message1 = MessageToUserEggs.objects.create(notification_to=test_user_manager1, \
                current_deal=test_object, notification_message=message)
        message2 = MessageToUserEggs.objects.create(notification_to=test_user_manager2, \
                current_deal=test_object, notification_message=message)
        message3 = MessageToUserEggs.objects.create(notification_to=test_user_manager1, \
                current_deal=test_object, notification_message=message)
        message4 = MessageToUserEggs.objects.create(notification_to=test_user_manager_b, \
                current_deal=test_object, notification_message=message)
        message5 = MessageToUserEggs.objects.create(notification_to=test_user_manager2, \
                current_deal=test_object, notification_message=message)
        message6 = MessageToUserEggs.objects.create(notification_to=test_user_manager_s, \
                current_deal=test_object, notification_message=message)
        message7 = MessageToUserEggs.objects.create(notification_to=test_user_manager1, \
                current_deal=test_object, notification_message=message)
        message8 = MessageToUserEggs.objects.create(notification_to=test_user_manager2, \
                current_deal=test_object, notification_message=message)
        search_done_deal_messages_and_turn_off_fields_is_value(test_object)
        current_deal_messages = MessageToUserEggs.objects.filter(current_deal=test_object) 
        self.assertEqual(current_deal_messages[0].is_active, False)        
        self.assertEqual(current_deal_messages[1].is_active, False)        
        self.assertEqual(current_deal_messages[2].is_active, False)        
        self.assertEqual(current_deal_messages[3].is_active, False)        
        self.assertEqual(current_deal_messages[4].is_active, False)        
        self.assertEqual(current_deal_messages[5].is_active, False)        
        self.assertEqual(current_deal_messages[6].is_active, False)        
        self.assertEqual(current_deal_messages[7].is_active, False)        

    def test_search_done_conf_calc_messages(self):
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
        message = 'test message'
        message1 = MessageToUserEggs.objects.create(notification_to=test_user_manager1, \
                current_conf_calculate=test_conf_calc, notification_message=message)
        message2 = MessageToUserEggs.objects.create(notification_to=test_user_manager2, \
                current_calculate=test_conf_calc.current_calculate, notification_message=message)
        message3 = MessageToUserEggs.objects.create(notification_to=test_user_manager1, \
                current_conf_calculate=test_conf_calc, notification_message=message)
        message4 = MessageToUserEggs.objects.create(notification_to=test_user_manager_b, \
                current_calculate=test_conf_calc.current_calculate, notification_message=message)
        message5 = MessageToUserEggs.objects.create(notification_to=test_user_manager2, \
                current_conf_calculate=test_conf_calc, notification_message=message)
        message6 = MessageToUserEggs.objects.create(notification_to=test_user_manager_s, \
                current_calculate=test_conf_calc.current_calculate, notification_message=message)
        message7 = MessageToUserEggs.objects.create(notification_to=test_user_manager1, \
                current_conf_calculate=test_conf_calc, notification_message=message)
        message8 = MessageToUserEggs.objects.create(notification_to=test_user_manager2, \
                current_calculate=test_conf_calc.current_calculate, notification_message=message)
        search_done_calc_and_conf_calc_messages_and_turn_off_fields_is_value(test_conf_calc)
        
        current_conf_calc_messages = MessageToUserEggs.objects.filter(current_conf_calculate=test_conf_calc) 
        current_calc_messages = MessageToUserEggs.objects.filter(current_calculate=test_conf_calc.current_calculate) 
        self.assertEqual(current_calc_messages[0].is_active, False)        
        self.assertEqual(current_calc_messages[1].is_active, False)        
        self.assertEqual(current_calc_messages[2].is_active, False)        
        self.assertEqual(current_calc_messages[3].is_active, False)        
        self.assertEqual(current_conf_calc_messages[0].is_active, False)        
        self.assertEqual(current_conf_calc_messages[1].is_active, False)        
        self.assertEqual(current_conf_calc_messages[2].is_active, False)        
        self.assertEqual(current_conf_calc_messages[3].is_active, False)        










