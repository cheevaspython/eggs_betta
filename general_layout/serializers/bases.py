from rest_framework import serializers

from general_layout.bases.models import BuyerCard, SellerCard, LogicCard


class SellerCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerCard
        fields = '__all__'


class BuyerCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuyerCard
        fields = '__all__'


class LogicCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogicCard
        fields = '__all__'


class SellerCardDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = SellerCard
        fields = ['name', 'inn', 'contact_person', 'phone', 'email', 'pay_type', 'comment']


class BuyerCardDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuyerCard
        fields = ['name', 'inn', 'contact_person', 'phone', 'email', 'pay_type', 'comment']


class LogicCardDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogicCard
        fields = ['name', 'inn', 'contact_person', 'phone', 'email', 'pay_type', 'comment']



