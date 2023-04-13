from rest_framework import serializers

from product_eggs.models.apps_eggs import ApplicationFromSellerBaseEggs, ApplicationFromBuyerBaseEggs
from product_eggs.serializers.base_card_serializers import SellerCardEggsDetailSerializer, \
    BuyerCardEggsDetailSerializer 
from users.serializers import CustomUserSerializer


class ApplicationSellerEggsDetailSerializer(serializers.ModelSerializer):
    seller_card_detail = SellerCardEggsDetailSerializer(read_only=True, source='current_seller')
    owner_detail = CustomUserSerializer(read_only=True, source='owner')
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])                      
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])                  
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от продавца')

    class Meta:
        model = ApplicationFromSellerBaseEggs
        fields = ['id', 'owner', 'delivery_window_from', 'delivery_window_until', 
            'c0', 'c0_cost', 'c1', 'c1_cost', 'c2', 'c2_cost', 'c3', 'c3_cost', 
            'cB', 'cB_cost', 'dirt', 'dirt_cost', 'current_seller', 'seller_card_detail',   
            'loading_address', 'comment', 'owner_detail', 'title', 'region',  
            'import_application', 'pre_payment_application', 'postponement_pay',  
        ]


class ApplicationBuyerEggsDetailSerializer(serializers.ModelSerializer):
    buyer_card_detail = BuyerCardEggsDetailSerializer(read_only=True, source='current_buyer')   
    owner_detail = CustomUserSerializer(read_only=True, source='owner')
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])                      
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])                  
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от покупателя')

    class Meta:
        model = ApplicationFromBuyerBaseEggs
        fields = ['id', 'owner', 'delivery_window_from', 'delivery_window_until', 
            'c0', 'c0_cost', 'c1', 'c1_cost', 'c2', 'c2_cost', 'c3', 'c3_cost', 
            'cB', 'cB_cost', 'dirt', 'dirt_cost', 'current_buyer', 'buyer_card_detail', 
            'unloading_address', 'comment', 'owner_detail', 'title', 'region', 
            'postponement_pay', 
        ]


class ApplicationSellerEggsSerializer(serializers.ModelSerializer):
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])                      
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])                  

    class Meta:
        model = ApplicationFromSellerBaseEggs
        fields = ['id', 'owner', 'delivery_window_from', 'delivery_window_until', 
            'c0', 'c0_cost', 'c1', 'c1_cost', 'c2', 'c2_cost', 'c3', 'c3_cost', 
            'dirt', 'dirt_cost', 'cB', 'cB_cost','region', 'loading_address',  
            'current_seller', 'import_application', 'pre_payment_application',
            'postponement_pay', 'comment',
        ]


class ApplicationBuyerEggsSerializer(serializers.ModelSerializer):
    delivery_window_from = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])                      
    delivery_window_until = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'])                  

    class Meta:
        model = ApplicationFromBuyerBaseEggs
        fields = ['id', 'owner', 'delivery_window_from', 'delivery_window_until', 
            'c0', 'c0_cost', 'c1', 'c1_cost', 'c2', 'c2_cost', 'c3', 'c3_cost', 
            'dirt', 'dirt_cost', 'current_buyer', 'region', 'postponement_pay', 
            'unloading_address', 'comment', 'cB', 'cB_cost',    
        ]


class ApplicationSellerEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от продавца')

    class Meta:
        model = ApplicationFromSellerBaseEggs
        fields = ['id', 'title', ]


class ApplicationBuyerEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Заявка от покупателя')

    class Meta:
        model = ApplicationFromBuyerBaseEggs
        fields = ['id', 'title', ]


