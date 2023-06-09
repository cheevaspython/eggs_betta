from rest_framework import serializers

from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs, LogicCardEggs
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.serializers.documents_serializers import DocumentsContractEggsSerializer


class RequisitesDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RequisitesEggs
        fields = '__all__'


class SellerCardEggsDetailSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesDetailSerializer(read_only=True, source='requisites')
    current_contract = DocumentsContractEggsSerializer(read_only=True, source='documents_contract')

    class Meta:
        model = SellerCardEggs
        fields = [
            'name', 'inn', 'contact_person', 'phone', 'email', 'comment', 'general_manager',
            'requisites', 'current_requisites', 'prod_address_1', 'prod_address_2', 
            'prod_address_3', 'prod_address_4', 'prod_address_5', 'documents_contract', 
            'current_contract', 'region', 'balance', 'manager',  
        ]


class SellerCardEggsPlusRequisitesSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesDetailSerializer(read_only=True, source='requisites')

    class Meta:
        model = SellerCardEggs
        fields = [
            'name', 'inn', 'contact_person', 'phone', 'email', 'comment', 'general_manager',
            'requisites', 'current_requisites', 'prod_address_1', 'prod_address_2', 
            'prod_address_3', 'prod_address_4', 'prod_address_5', 'documents_contract', 
            'region', 'balance', 'manager',  
        ]


class BuyerCardEggsDetailSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesDetailSerializer(read_only=True, source='requisites')
    current_contract = DocumentsContractEggsSerializer(read_only=True, source='documents_contract')

    class Meta:
        model = BuyerCardEggs
        fields = [
            'name', 'inn', 'contact_person', 'phone', 'email', 'comment', 'general_manager', 
            'requisites', 'current_requisites', 'warehouse_address_1', 'warehouse_address_2', 
            'warehouse_address_3', 'warehouse_address_4', 'warehouse_address_5', 'documents_contract',
            'current_contract', 'pay_limit', 'region', 'balance_form_one', 'balance_form_one', 
            'manager', 'pay_limit_cash', 'balance',   
        ]


class BuyerCardEggsPlusRequisitesSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesDetailSerializer(read_only=True, source='requisites')

    class Meta:
        model = BuyerCardEggs
        fields = [
            'name', 'inn', 'contact_person', 'phone', 'email', 'comment', 'general_manager', 
            'requisites', 'current_requisites', 'warehouse_address_1', 'warehouse_address_2', 
            'warehouse_address_3', 'warehouse_address_4', 'warehouse_address_5', 'documents_contract',
            'pay_limit', 'region', 'balance_form_one', 'balance_form_one', 
            'manager', 'pay_limit_cash', 'balance',   
        ]


class LogicCardEggsDetailSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesDetailSerializer(read_only=True, source='requisites')
    current_contract = DocumentsContractEggsSerializer(read_only=True, source='documents_contract')

    class Meta:
        model = LogicCardEggs
        fields = [
            'name', 'inn', 'contact_person', 'phone', 'email', 'comment', 
            'requisites', 'current_requisites', 'documents_contract', 'general_manager',
            'balance_form_one', 'balance_form_one', 'balance', 'current_contract', 
        ]


# class LogicCardEggsPlusRequisitesSerializer(serializers.ModelSerializer):
#     current_requisites = RequisitesDetailSerializer(read_only=True, source='requisites')
#
#     class Meta:
#         model = LogicCardEggs
#         fields = [
#             'name', 'inn', 'contact_person', 'phone', 'email', 'comment', 
#             'requisites', 'current_requisites', 'documents_contract', 'general_manager',
#             'balance_form_one', 'balance_form_one', 'balance',  
#         ]


class SellerCardEggsSerializerBukh(serializers.ModelSerializer):

    class Meta:
        model = SellerCardEggs
        fields = [
            'name', 'inn',# 'title'   
        ]


class BuyerCardEggsSerializerBukh(serializers.ModelSerializer):

    class Meta:
        model = BuyerCardEggs
        fields = [
            'name', 'inn',# 'title'   
        ]


class LogicCardEggsSerializerBukh(serializers.ModelSerializer):

    class Meta:
        model = LogicCardEggs
        fields = [
            'name', 'inn',# 'title'   
        ]
