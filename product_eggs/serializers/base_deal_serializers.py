from rest_framework import serializers

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.documents_serializers import DocumentsDealGetEggsSerializer


class CalculateEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            
            'cash', 'import_application', 

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ]


class CalculateEggsNamesSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    owner_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()

    def get_owner_name(self, instance):
        return instance.owner.username

    def get_buyer_name(self, instance):
        return instance.buyer.name

    def get_seller_name(self, instance):
        return instance.seller.name

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            
            'cash', 'import_application', 

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ] + [
            'owner_name', 'buyer_name', 'seller_name'
        ]


class ConfirmedCalculateEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'current_logic', 'additional_expense', 'documents',
            
            'cash', 'import_application', 
            'calc_ready', 'logic_confirmed',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ]


class ConfirmedCalculateEggsNameSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    owner_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    expense_total = serializers.SerializerMethodField()
    expense_detail_json = serializers.SerializerMethodField()
    logic_name = serializers.SerializerMethodField()
    logic_inn = serializers.SerializerMethodField()

    def get_expense_total(self, instance):
        return instance.additional_expense.expense_total

    def get_expense_detail_json(self, instance):
        return instance.additional_expense.expense_detail_json

    def get_owner_name(self, instance):
        return instance.owner.username

    def get_buyer_name(self, instance):
        return instance.buyer.name

    def get_seller_name(self, instance):
        return instance.seller.name

    def get_logic_name(self, instance):
        return instance.current_logic.name
    
    def get_logic_inn(self, instance):
        return instance.current_logic.inn

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'current_logic', 'additional_expense', 'documents',
            
            'cash', 'import_application', 
            'calc_ready', 'logic_confirmed',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json',
        ]


class BaseDealEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    actual_loading_date = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    actual_unloading_date = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'current_logic', 'additional_expense', 'documents',
            
            'cash', 'import_application', 
            'calc_ready', 'logic_confirmed', 'deal_status_ready_to_change',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address', 
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount', 
            'deal_buyer_pay_amount', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD', 


            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ]


class BaseDealEggsNameSerializer(serializers.ModelSerializer):

    documents_detail = DocumentsDealGetEggsSerializer(read_only=True, source='documents')
    owner_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    expense_total = serializers.SerializerMethodField()
    expense_detail_json = serializers.SerializerMethodField()
    logic_name = serializers.SerializerMethodField()
    logic_inn = serializers.SerializerMethodField()

    def get_expense_total(self, instance):
        return instance.additional_expense.expense_total

    def get_expense_detail_json(self, instance):
        return instance.additional_expense.expense_detail_json

    def get_owner_name(self, instance):
        return instance.owner.username

    def get_buyer_name(self, instance):
        return instance.buyer.name

    def get_seller_name(self, instance):
        return instance.seller.name

    def get_logic_name(self, instance):
        return instance.current_logic.name
    
    def get_logic_inn(self, instance):
        return instance.current_logic.inn

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'current_logic', 'additional_expense', 'documents',
            
            'cash', 'import_application', 
            'calc_ready', 'logic_confirmed', 

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address', 
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer',  
            'deal_our_debt_UPD', 'deal_buyer_debt_UPD', 
            'deal_buyer_pay_amount', 'deal_our_pay_amount',

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json', 'documents_detail',
        ]


class CompleteDealEggsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status', 'is_active',

            'log_status_calc_query', 'log_status_conf_calc_query',
            'log_status_deal_query',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'current_logic', 'additional_expense', 'documents',
            
            'cash', 'import_application', 
            'calc_ready', 'logic_confirmed', 'deal_status_ready_to_change',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address', 
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount', 
            'deal_buyer_pay_amount', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD', 

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ]

class BaseCompDealEggsNameSerializer(serializers.ModelSerializer):

    documents_detail = DocumentsDealGetEggsSerializer(read_only=True, source='documents')
    owner_name = serializers.SerializerMethodField()
    buyer_name = serializers.SerializerMethodField()
    seller_name = serializers.SerializerMethodField()
    expense_total = serializers.SerializerMethodField()
    expense_detail_json = serializers.SerializerMethodField()
    logic_name = serializers.SerializerMethodField()
    logic_inn = serializers.SerializerMethodField()

    def get_expense_total(self, instance):
        return instance.additional_expense.expense_total

    def get_expense_detail_json(self, instance):
        return instance.additional_expense.expense_detail_json

    def get_owner_name(self, instance):
        return instance.owner.username

    def get_buyer_name(self, instance):
        return instance.buyer.name

    def get_seller_name(self, instance):
        return instance.seller.name

    def get_logic_name(self, instance):
        return instance.current_logic.name
    
    def get_logic_inn(self, instance):
        return instance.current_logic.inn

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status', 'is_active',

            'log_status_calc_query', 'log_status_conf_calc_query',
            'log_status_deal_query',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'current_logic', 'additional_expense', 'documents',
            
            'cash', 'import_application', 
            'calc_ready', 'logic_confirmed', 'deal_status_ready_to_change',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address', 
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount', 
            'deal_buyer_pay_amount', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD', 

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json', 'documents_detail',
        ]


class BaseDealBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'deal_buyer_pay_amount', 'documents', 'cash', 'logic_our_debt_UPD',
            'deal_buyer_debt_UPD', 'payback_day_for_us', 'payback_day_for_buyer', 
            'deal_our_pay_amount', 'deal_our_debt_UPD', 'logic_our_pay_amount',
            'logic_our_debt_for_app_contract', 'delivery_form_payment',
        ]


class CalculateEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Просчет')

    class Meta:
        model = BaseDealEggsModel
        fields = ['id', 'title',]


class ConfirmedCalculateEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Подтвержденный просчет')

    class Meta:
        model = BaseDealEggsModel
        fields = ['id', 'title',]


class DealEggsSerializerSideBar(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    model_id = serializers.IntegerField()

    def get_title(self, instance):
        return ('Сделка')

    class Meta:
        model = BaseDealEggsModel
        fields = ['id', 'title',] + ['model_id']


class BaseDealEggsSerializerWsSideBar(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    actual_loading_date = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    actual_unloading_date = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)
    title = serializers.SerializerMethodField()
    model_id = serializers.SerializerMethodField()

    def get_title(self, instance):
        return ('Сделка')

    def get_model_id(self, instance):
        return (instance.documents.pk)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',
            'deal_status',

            'application_from_buyer', 'application_from_seller',
            'buyer', 'seller', 'owner',
            'current_logic', 'additional_expense', 'documents',
            
            'cash', 'import_application', 
            'calc_ready', 'logic_confirmed', 'deal_status_ready_to_change',

            'delivery_cost', 'delivery_by_seller',
            'delivery_form_payment', 'delivery_type_of_payment',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address', 
            'actual_loading_date', 'actual_unloading_date',

            'logic_our_debt_for_app_contract', 'logic_our_pay_amount',
            'logic_our_debt_UPD',
            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'deal_our_pay_amount', 
            'deal_buyer_pay_amount', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD', 


            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ] + ['title', 'model_id']
