import logging
from rest_framework import serializers

from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs, LogicCardEggs
from product_eggs.serializers.balance_serializers import BalanceBaseClientEggsSerializer
from product_eggs.serializers.contact_person_serializers import ContactPersonEggsSerializer
from product_eggs.serializers.documents_serializers import DocumentsContractEggsSerializer
from product_eggs.serializers.entity_serializers import EntityEggsModelSerializer
from product_eggs.serializers.requisites_serializers import RequisitesEggsModelSerializer

logger = logging.getLogger(__name__)


class SellerCardEggsDetailSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesEggsModelSerializer(read_only=True, source='requisites')
    current_contract = DocumentsContractEggsSerializer(read_only=True, source='documents_contract')
    current_contact_persons = ContactPersonEggsSerializer(read_only=True, many=True, source='contact_person')
    manager_name = serializers.SerializerMethodField()
    current_balances = serializers.SerializerMethodField()

    def get_current_balances(self, instance):
        balances = instance.cur_balance.all()
        if balances:
            return_data = []
            for balance in balances:
                return_data.append(BalanceBaseClientEggsSerializer(balance).data)
            return return_data

    def get_manager_name(self, instance):
        try:
            return instance.manager.username
        except Exception as e:
            logger.debug('base_serializer: cant get manager username', e)
            return None

    class Meta:
        model = SellerCardEggs
        fields = [
            'inn', 'contact_person', 'comment',
            'requisites', 'current_requisites', 'prod_address_1', 'prod_address_2',
            'prod_address_3', 'prod_address_4', 'prod_address_5', 'documents_contract',
            'current_contract', 'region', 'manager', 'manager_name',
            'resident', 'link', 'current_contact_persons',
            'current_balances',
        ]


class SellerCardEggsPlusRequisitesSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesEggsModelSerializer(read_only=True, source='requisites')
    current_contract = DocumentsContractEggsSerializer(read_only=True, source='documents_contract')

    class Meta:
        model = SellerCardEggs
        fields = [
            'inn', 'contact_person', 'comment',
            'requisites', 'current_requisites', 'prod_address_1', 'prod_address_2',
            'prod_address_3', 'prod_address_4', 'prod_address_5', 'documents_contract',
            'region', 'manager', 'resident', 'link', 'current_contract',
        ]


class BuyerCardEggsDetailSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesEggsModelSerializer(read_only=True, source='requisites')
    current_contract = DocumentsContractEggsSerializer(read_only=True, source='documents_contract')
    current_contact_persons = ContactPersonEggsSerializer(read_only=True, many=True, source='contact_person')
    manager_name = serializers.SerializerMethodField()
    current_balances = serializers.SerializerMethodField()

    def get_current_balances(self, instance):
        balances = instance.cur_balance.all()
        if balances:
            return_data = []
            for balance in balances:
                return_data.append(BalanceBaseClientEggsSerializer(balance).data)
            return return_data

    def get_manager_name(self, instance):
        try:
            return instance.manager.username
        except Exception as e:
            logger.debug('base_serializer: cant get manager username', e)
            return None

    class Meta:
        model = BuyerCardEggs
        fields = [
            'inn', 'contact_person', 'comment',
            'requisites', 'current_requisites', 'warehouse_address_1', 'warehouse_address_2',
            'warehouse_address_3', 'warehouse_address_4', 'warehouse_address_5', 'documents_contract',
            'current_contract', 'region', 'manager', 'manager_name',
            'resident', 'link', 'current_contact_persons',
            'current_balances',
        ]


class BuyerCardEggsPlusRequisitesSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesEggsModelSerializer(read_only=True, source='requisites')
    current_contract = DocumentsContractEggsSerializer(read_only=True, source='documents_contract')

    class Meta:
        model = BuyerCardEggs
        fields = [
            'inn', 'contact_person', 'comment',
            'requisites', 'current_requisites', 'warehouse_address_1', 'warehouse_address_2',
            'warehouse_address_3', 'warehouse_address_4', 'warehouse_address_5', 'documents_contract',
            'region', 'manager', 'resident', 'link', 'current_contract',
        ]


class LogicCardEggsDetailSerializer(serializers.ModelSerializer):
    current_requisites = RequisitesEggsModelSerializer(read_only=True, source='requisites')
    current_contract = DocumentsContractEggsSerializer(read_only=True, source='documents_contract')
    current_contact_persons = ContactPersonEggsSerializer(read_only=True, many=True, source='contact_person')
    manager_name = serializers.SerializerMethodField()
    current_balances = serializers.SerializerMethodField()

    def get_current_balances(self, instance):
        balances = instance.cur_balance.all()
        if balances:
            return_data = []
            for balance in balances:
                return_data.append(BalanceBaseClientEggsSerializer(balance).data)
            return return_data

    def get_manager_name(self, instance):
        try:
            return instance.manager.username
        except Exception as e:
            logger.debug('base_serializer: cant get manager username', e)
            return None

    class Meta:
        model = LogicCardEggs
        fields = [
            'inn', 'contact_person', 'comment', 'region', 'manager',
            'requisites', 'current_requisites', 'documents_contract',
            'resident', 'link', 'current_contact_persons', 'manager_name',
            'current_contract',
            'current_balances',
        ]


# class ClientCardEggsSerializerBukh(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()
#     balances = serializers.SerializerMethodField()
#
#     def get_name(self, instance):
#         return instance.requisites.name
#
#     def get_balances(self, instance):
#         return list(instance.cur_balance.only('entity').values_list('entity', flat=True))


class SellerCardEggsSerializerBukh(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = SellerCardEggs
        fields = [
            'inn', 'name', 'entitys',
        ]


class BuyerCardEggsSerializerBukh(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = BuyerCardEggs
        fields = [
            'inn', 'name', 'entitys',
        ]


class LogicCardEggsSerializerBukh(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = LogicCardEggs
        fields = [
            'inn', 'name', 'entitys',
        ]
