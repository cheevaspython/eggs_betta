# from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from product_eggs.models.base_eggs import BuyerCardEggs
from product_eggs.serializers.base_card_serializers import BuyerCardEggsDetailSerializer


class BuyerCardEggsTestCase(APITestCase):
    def test_get(self):
        buyer_card_1 = BuyerCardEggs.objects.create(name='test buyer 1', inn='109238')
        buyer_card_2 = BuyerCardEggs.objects.create(name='test buyer 2', inn='109239')
        url = 'http://127.0.0.1:8000/api/eggs/buyer_card/'
        response = self.client.get(url)
        serializer_data = BuyerCardEggsDetailSerializer([buyer_card_1, buyer_card_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

        
        
