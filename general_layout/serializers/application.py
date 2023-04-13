from rest_framework import serializers

from general_layout.application.models import ApplicationFromSellerBase, ApplicationFromBuyerBase
from general_layout.serializers.bases import SellerCardDetailSerializer, BuyerCardDetailSerializer


class ApplicationSellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationFromSellerBase
        fields = ['id', 'owner', 'current_seller']


class ApplicationBuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicationFromBuyerBase
        fields = ['id', 'owner', 'current_buyer']


class ApplicationSellerDetailSerializer(serializers.ModelSerializer):
    seller_card_detail = SellerCardDetailSerializer(read_only=True, source='seller_card_detail')

    class Meta:
        model = ApplicationFromSellerBase
        fields = ['id', 'owner', 'current_seller', 'seller_card_detail']


class ApplicationBuyerDetailSerializer(serializers.ModelSerializer):
    buyer_card_detail = BuyerCardDetailSerializer(read_only=True, source='buyer_card_detail')   

    class Meta:
        model = ApplicationFromBuyerBase
        fields = ['id', 'owner', 'current_buyer', 'buyer_card_detail']

