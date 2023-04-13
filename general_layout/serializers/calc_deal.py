from rest_framework import serializers

from general_layout.calculate_and_deal.models import Calculate, ConfirmedCalculate, Deal
from general_layout.serializers.application import ApplicationSellerDetailSerializer, ApplicationBuyerDetailSerializer
from general_layout.serializers.bases import LogicCardDetailSerializer


class CalculateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Calculate
        fields = ['id', 'application_from_buyer', 'application_from_seller', 'average_delivery_cost']


class ConfirmedCalculateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ConfirmedCalculate
        fields = [
            'id', 'current_calculate', 'current_logic', 'delivery_date_from_seller',
            'delivery_date_to_buyer', 'delivery_cost', 'calc_ready',
        ]


class CalculateDetailSerializer(serializers.ModelSerializer):
    application_seller_detail = ApplicationSellerDetailSerializer(read_only=False, source='application_from_seller')
    application_buyer_detail = ApplicationBuyerDetailSerializer(read_only=False, source='application_from_buyer')

    class Meta:
        model = Calculate
        fields = [
                'id', 'application_from_buyer', 'application_from_seller',
                'average_delivery_cost', 'application_buyer_detail',
                'application_seller_detail', 
        ]


class ConfirmedCalculateDetailSerializer(serializers.ModelSerializer):
    calculate_detail = CalculateDetailSerializer(read_only=False, source='calculate_detail')
    logic_detail = LogicCardDetailSerializer(read_only=False, source='logic_detail')

    class Meta:
        model = ConfirmedCalculate
        fields = [
            'id', 'current_calculate', 'current_logic', 'delivery_date_from_seller', 'delivery_date_to_buyer',
             'delivery_cost', 'calc_ready', 'calculate_detail', 'logic_detail',
        ]


class DealSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deal
        fields = ['id', 'status', 'confirmed_calculate', 'processing_to_confirm']


class DealDetailSerializer(serializers.ModelSerializer):
    confirmed_calculate_detail = ConfirmedCalculateDetailSerializer(read_only=False, source='confirmed_calculate')

    class Meta:
        model = Deal
        fields = ['id', 'status', 'confirmed_calculate', 'processing_to_confirm', 'confirmed_calculate_detail']















