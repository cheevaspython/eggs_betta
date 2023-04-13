from rest_framework import serializers

from product_eggs.models.calcs_deal_eggs import CalculateEggs, ConfirmedCalculateEggs, DealEggs
from product_eggs.serializers.base_card_serializers import LogicCardEggsDetailSerializer
from product_eggs.serializers.additional_expense_serializer import AdditionalExpenseEggsDetailSerializer
from product_eggs.serializers.documents_serializers import DocumentsDealEggsSerializer
from product_eggs.services.deal_services import get_additional_exp_detail


class CalculateEggsDetailSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    title = serializers.SerializerMethodField()
    margin = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()

    def get_owner_name(self, instance):
        return f'{instance.owner.first_name} {instance.owner.last_name}'

    def get_margin(self, instance):
        try:
            return instance.margin
        except AttributeError:
            return 0

    def get_title(self, instance):
        return ('Просчет')

    class Meta:
        model = CalculateEggs
        fields = [
            'id', 'application_from_buyer', 'application_from_seller',
            'delivery_cost', 'comment', 'title', 'import_application', 'owner', 'cash',
            'cB', 'seller_cB_cost', 'buyer_cB_cost','c0', 'seller_c0_cost','buyer_c0_cost',
            'c1', 'seller_c1_cost', 'buyer_c1_cost', 'c2', 'seller_c2_cost', 'buyer_c2_cost',
            'c3', 'seller_c3_cost', 'seller_c3_cost', 'buyer_c3_cost', 'dirt', 'seller_dirt_cost', 
            'buyer_dirt_cost', 'delivery_type_of_payment', 'delivery_date_to_buyer',
            'margin', 'delivery_date_from_seller', 'seller_inn', 'buyer_inn',
            'loading_address', 'unloading_address', 'seller_name', 'buyer_name',  
            'note', 'owner_name', 'pre_payment_application', 'import_application',
            'delivery_by_seller', 'postponement_pay_for_us', 'postponement_pay_for_buyer',
        ]


class CalculateEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    owner_name = serializers.SerializerMethodField()

    def get_owner_name(self, instance):
        return f'{instance.owner.first_name} {instance.owner.last_name}'

    class Meta:
        model = CalculateEggs
        fields = [
            'id', 'application_from_buyer', 'application_from_seller',
            'delivery_cost', 'comment', 'delivery_type_of_payment',
            'seller_name', 'buyer_name', 'cB', 'seller_cB_cost', 'buyer_cB_cost',
            'c0', 'seller_c0_cost', 'buyer_c0_cost', 'c1', 'seller_c1_cost',
            'buyer_c1_cost', 'c2', 'seller_c2_cost', 'buyer_c2_cost', 'c3',
            'seller_c3_cost', 'buyer_c3_cost', 'dirt', 'seller_dirt_cost', 'cash',
            'buyer_dirt_cost', 'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'delivery_by_seller', 'import_application', 'loading_address', 'unloading_address', 
            'seller_inn', 'buyer_inn', 'note', 'owner_name', 'pre_payment_application',
            'postponement_pay_for_us', 'postponement_pay_for_buyer',
        ]


class ConfirmedCalculateEggsDetailSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    calculate_detail = CalculateEggsDetailSerializer(read_only=True, source='current_calculate')
    logic_detail = LogicCardEggsDetailSerializer(read_only=True, source='current_logic')
    additional_expense_detail = AdditionalExpenseEggsDetailSerializer(read_only=True, source='additional_expense')
    title = serializers.SerializerMethodField()
    margin = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()

    def get_owner_name(self, instance):
        return f'{instance.owner.first_name} {instance.owner.last_name}'

    def get_margin(self, instance):
        try:
            return instance.margin
        except AttributeError:
            return 0

    def get_title(self, instance):
        return ('Подтвержденный просчет')

    class Meta:
        model = ConfirmedCalculateEggs
        fields = [
            'id', 'current_calculate', 'current_logic', 'title', 
            'calc_ready', 'calculate_detail', 'logic_detail', 'comment',
            'additional_expense', 'additional_expense_detail', 'margin',
            'owner_name', 'delivery_cost', 'note', 'delivery_type_of_payment',
            'logic_confirmed', 'delivery_date_from_seller', 'delivery_date_to_buyer',
        ]


class ConfirmedCalculateEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)

    class Meta:
        model = ConfirmedCalculateEggs
        fields = [
            'id', 'current_calculate', 'current_logic', 'comment',  
            'additional_expense', 'calc_ready', 'delivery_cost', 'note',  
            'delivery_type_of_payment', 'logic_confirmed', 'delivery_date_from_seller',
            'delivery_date_to_buyer',
        ]


class DealEggsDetailSerializer(serializers.ModelSerializer):
    delivery_date_from_seller_from_calc = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer_from_calc = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    documents_detail = DocumentsDealEggsSerializer(read_only=True, source='documents')
    actual_loading_date = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    actual_unloading_date = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)

    logic_detail = LogicCardEggsDetailSerializer(read_only=True, source='current_logic')

    owner_name = serializers.SerializerMethodField()
    additional_expense_detail = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    margin = serializers.SerializerMethodField()

    def get_additional_expense_detail(self, instance):
        return get_additional_exp_detail(instance)

    def get_owner_name(self, instance):
        return f'{instance.owner.first_name} {instance.owner.last_name}'

    def get_margin(self, instance):
        try:
            return instance.margin
        except AttributeError:
            return 0

    def get_title(self, instance):
        return ('Сделка')

    class Meta:
        model = DealEggs
        fields = [
            'id', 'status', 'confirmed_calculate', 'processing_to_confirm',  
            'owner_name', 'comment', 'documents', 'additional_expense_detail',
            'actual_loading_date', 'actual_unloading_date', 'margin', 'documents_detail',
            'current_logic', 'additional_expense', 'cB', 'seller_cB_cost','buyer_cB_cost', 
            'c0', 'seller_c0_cost', 'buyer_c0_cost', 'c1', 'seller_c1_cost', 'buyer_c1_cost',
            'c2', 'seller_c2_cost', 'buyer_c2_cost', 'c3',  'seller_c3_cost', 'buyer_c3_cost', 
            'dirt', 'seller_manager', 'buyer_dirt_cost', 'buyer_manager', 'delivery_cost',  
            'seller_dirt_cost', 'logic_detail', 'delivery_type_of_payment', 'delivery_by_seller',
            'seller_inn', 'buyer_inn','title', 'seller_name', 'buyer_name', 'cash',
            'delivery_date_to_buyer_from_calc', 'delivery_date_from_seller_from_calc',
            'loading_address', 'unloading_address', 'payback_day_for_us', 'payback_day_for_buyer',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'pre_payment_application',
            'import_application', 'current_deal_our_debt', 'current_deal_buyer_debt',
            'deal_our_debt_UPD', 'deal_buyer_debt_UPD',
        ]


class DealEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller_from_calc = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer_from_calc = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    actual_loading_date = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    actual_unloading_date = serializers.DateField(input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)

    class Meta:
        model = DealEggs
        fields = [
            'id', 'status', 'confirmed_calculate', 'processing_to_confirm',
            'comment', 'actual_loading_date', 'actual_unloading_date', 'documents',
            'cB', 'seller_cB_cost', 'buyer_cB_cost', 'c0', 'seller_c0_cost', 'buyer_c0_cost',
            'c1', 'seller_c1_cost', 'buyer_c1_cost', 'c2', 'seller_c2_cost', 'buyer_c2_cost', 'c3',
            'seller_c3_cost', 'buyer_c3_cost', 'dirt', 'buyer_dirt_cost', 'seller_dirt_cost', 
            'buyer_manager', 'seller_manager', 'delivery_cost', 'delivery_type_of_payment',
            'seller_inn', 'buyer_inn', 'seller_name', 'buyer_name', 'cash', 'additional_expense',
            'current_logic', 'delivery_date_from_seller_from_calc', 'delivery_date_to_buyer_from_calc', 
            'loading_address', 'unloading_address', 'delivery_by_seller', 'payback_day_for_us', 
            'payback_day_for_buyer', 'postponement_pay_for_buyer', 'postponement_pay_for_us', 
            'import_application', 'pre_payment_application', 'current_deal_our_debt',
            'current_deal_buyer_debt', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD',
    ]


class CalculateEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Просчет')

    class Meta:
        model = CalculateEggs
        fields = ['id', 'title',]


class ConfirmedCalculateEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Подтвержденный просчет')

    class Meta:
        model = ConfirmedCalculateEggs
        fields = ['id', 'title',]


class DealEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Сделка')

    class Meta:
        model = DealEggs
        fields = ['id', 'title',]


class DealEggsSerializerDebtBuyer(serializers.ModelSerializer):

    class Meta:
        model = DealEggs
        fields = [
            'id', 'current_deal_buyer_debt', 'documents', 'cash',
            'deal_buyer_debt_UPD', 'payback_day_for_us', 'payback_day_for_buyer', 
        ]

