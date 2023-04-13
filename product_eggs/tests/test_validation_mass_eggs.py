from django.test import TestCase
from rest_framework import exceptions

from product_eggs.serializers.apps_serializers_eggs import ApplicationSellerEggsDetailSerializer
from product_eggs.models.apps_eggs import  ApplicationFromSellerBaseEggs
from product_eggs.models.base_eggs import SellerCardEggs, RequisitesEggs
from product_eggs.services.validation_of_mass_egg import validation_of_maximum_mass_eggs
from users.models import CustomUser


class ValidationOfMaxMassTestCase(TestCase):

    def test_validation_max_mass_eggs_overmass(self):
        test_requisites1 = RequisitesEggs.objects.create(general_manager='test1') 
        test_user_manager_s = CustomUser.objects.create(username='tester_s', role=1)
        test_seller = SellerCardEggs.objects.create(name='test_seller', requisites=test_requisites1)
        test_app_seller = ApplicationFromSellerBaseEggs.objects.create(owner=test_user_manager_s, c0=100, c0_cost=10, c1=80, c1_cost=50, \
            c2=4000, c2_cost=50, c3=10000, c3_cost=90, dirt=0, dirt_cost=0, current_seller=test_seller)
        test_validate_data = ApplicationSellerEggsDetailSerializer(test_app_seller).data 
         
        self.assertRaises(exceptions.ValidationError, validation_of_maximum_mass_eggs, \
                test_validate_data)
