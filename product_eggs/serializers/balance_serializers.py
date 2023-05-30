from rest_framework import serializers

from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.serializers.base_client_serializers import RequisitesDetailSerializer
from product_eggs.serializers.base_deal_serializers import BaseDealEggsSerializer


class StatisticBuyerClientSerializer(serializers.ModelSerializer):
    debt_deals = BaseDealEggsSerializer(source='basedealeggsmodel_set', many=True)
    current_requisites = RequisitesDetailSerializer(read_only=True, source='requisites')
    
    class Meta:
        model = BuyerCardEggs
        depth = 1
        fields = '__all__'


class StatisticSellerClientSerializer(serializers.ModelSerializer):
    debt_deals = BaseDealEggsSerializer(source='basedealeggsmodel_set', many=True)
    current_requisites = RequisitesDetailSerializer(read_only=True, source='requisites')
    
    class Meta:
        model = SellerCardEggs
        depth = 1
        fields = '__all__'


class StatisticLogicClientSerializer(serializers.ModelSerializer):
    debt_deals = BaseDealEggsSerializer(source='basedealeggsmodel_set', many=True)
    current_requisites = RequisitesDetailSerializer(read_only=True, source='requisites')
    
    class Meta:
        model = LogicCardEggs
        depth = 1
        fields = '__all__'

