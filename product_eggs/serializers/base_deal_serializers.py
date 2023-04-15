from rest_framework import serializers

from product_eggs.models.base_deal import BaseDealEggsModel


class CalculateEggsSerializer(serializers.ModelSerializer):
    delivery_date_from_seller = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)                      
    delivery_date_to_buyer = serializers.DateField(
        input_formats=['%d/%m/%Y', '%d.%m.%Y', 'iso-8601'], required=False)

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 

            'application_from_buyer', 'application_from_seller', 'buyer', 'seller', 'owner',
            
            'cash', 'import_application', 

            'delivery_cost', 'delivery_type_of_payment', 'delivery_by_seller',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ]


class CustomCalculateSerializer(serializers.ModelSerializer):

    buyer_name = serializers.CharField()
    seller_name = serializers.CharField()
    owner_name = serializers.CharField()

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 

            'application_from_buyer', 'application_from_seller', 'buyer', 'seller', 'owner',
            
            'cash', 'import_application', 

            'delivery_cost', 'delivery_type_of_payment', 'delivery_by_seller',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name',
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

            'application_from_buyer', 'application_from_seller', 'buyer', 'seller', 'owner',
            'current_logic', 'additional_expense', 
            
            'cash', 'import_application', 
            'calc_ready', 'logic_confirmed',

            'delivery_cost', 'delivery_type_of_payment', 'delivery_by_seller',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ]


class CustomConfCalcEggsSerializer(serializers.ModelSerializer):

    buyer_name = serializers.CharField()
    seller_name = serializers.CharField()
    owner_name = serializers.CharField()
    expense_total = serializers.FloatField()
    expense_detail_json = serializers.JSONField()   #mb lag
    logic_name = serializers.CharField()
    logic_inn = serializers.CharField()

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'status', 'comment', 'note_calc', 'note_conf_calc',

            'application_from_buyer', 'application_from_seller', 'buyer', 'seller', 'owner',
            'current_logic', 'additional_expense', 
            
            'cash', 'import_application', 
            'calc_ready', 'logic_confirmed',

            'delivery_cost', 'delivery_type_of_payment', 'delivery_by_seller',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address',

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

            'delivery_cost', 'delivery_type_of_payment', 'delivery_by_seller',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address', 
            'actual_loading_date', 'actual_unloading_date',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'current_deal_our_debt', 
            'current_deal_buyer_debt', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD', 

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ]


class CustomBaseDealEggsSerializer(serializers.ModelSerializer):

    buyer_name = serializers.CharField()
    seller_name = serializers.CharField()
    owner_name = serializers.CharField()
    expense_total = serializers.FloatField()
    expense_detail_json = serializers.JSONField()   #mb lag
    logic_name = serializers.CharField()
    logic_inn = serializers.CharField()

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

            'delivery_cost', 'delivery_type_of_payment', 'delivery_by_seller',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address', 
            'actual_loading_date', 'actual_unloading_date',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer',  
            'deal_our_debt_UPD', 'deal_buyer_debt_UPD', 
            'current_deal_buyer_debt', 'current_deal_our_debt',

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json',
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

            'delivery_cost', 'delivery_type_of_payment', 'delivery_by_seller',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address', 
            'actual_loading_date', 'actual_unloading_date',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'current_deal_our_debt', 
            'current_deal_buyer_debt', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD', 

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ]

class CustomBaseCompDealEggsSerializer(serializers.ModelSerializer):

    buyer_name = serializers.CharField()
    seller_name = serializers.CharField()
    owner_name = serializers.CharField()
    expense_total = serializers.FloatField()
    expense_detail_json = serializers.JSONField()   #mb lag
    logic_name = serializers.CharField()
    logic_inn = serializers.CharField()

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

            'delivery_cost', 'delivery_type_of_payment', 'delivery_by_seller',
            'delivery_date_from_seller', 'delivery_date_to_buyer', 
            'loading_address', 'unloading_address', 
            'actual_loading_date', 'actual_unloading_date',

            'postponement_pay_for_us', 'postponement_pay_for_buyer', 'margin',
            'payback_day_for_us', 'payback_day_for_buyer', 'current_deal_our_debt', 
            'current_deal_buyer_debt', 'deal_our_debt_UPD', 'deal_buyer_debt_UPD', 

            'cB', 'c0', 'c1', 'c2', 'c3', 'dirt',
            'seller_cB_cost', 'seller_c0_cost', 'seller_c1_cost',
            'seller_c2_cost', 'seller_c3_cost', 'seller_dirt_cost',
            'buyer_cB_cost', 'buyer_c0_cost', 'buyer_c1_cost', 'buyer_c2_cost',
            'buyer_c3_cost', 'buyer_dirt_cost',
        ] + [
            'buyer_name', 'seller_name', 'owner_name', 'logic_name', 'logic_inn',
            'expense_total', 'expense_detail_json',
        ]


class BaseDealBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = BaseDealEggsModel
        fields = [
            'id', 'current_deal_buyer_debt', 'documents', 'cash',
            'deal_buyer_debt_UPD', 'payback_day_for_us', 'payback_day_for_buyer', 
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

    def get_title(self, instance):
        return ('Сделка')

    class Meta:
        model = BaseDealEggsModel
        fields = ['id', 'title',]
