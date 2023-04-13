from rest_framework import serializers


class DealEggsSerializerRaw(serializers.Serializer):

    id = serializers.IntegerField()
    status = serializers.IntegerField()
    confirmed_calculate_id = serializers.IntegerField()
    comment = serializers.CharField()
    documents_id = serializers.IntegerField()
    actual_loading_date = serializers.DateField()
    actual_unloading_date = serializers.DateField()
    cB = serializers.IntegerField()
    seller_cB_cost = serializers.FloatField()
    buyer_cB_cost = serializers.FloatField()
    c0 = serializers.IntegerField()
    seller_c0_cost = serializers.FloatField()
    buyer_c0_cost =serializers.FloatField()
    c1 = serializers.IntegerField()
    seller_c1_cost = serializers.FloatField()
    buyer_c1_cost = serializers.FloatField()
    c2 = serializers.IntegerField()
    seller_c2_cost = serializers.FloatField()
    buyer_c2_cost = serializers.FloatField()
    c3 = serializers.IntegerField()
    seller_c3_cost = serializers.FloatField()
    buyer_c3_cost = serializers.FloatField()
    dirt = serializers.IntegerField()
    seller_dirt_cost = serializers.FloatField()
    buyer_dirt_cost = serializers.FloatField()
    seller_manager_id = serializers.IntegerField()
    buyer_manager_id = serializers.IntegerField()
    delivery_cost = serializers.FloatField()
    delivery_type_of_payment = serializers.IntegerField()
    seller_inn = serializers.CharField()
    buyer_inn = serializers.CharField()
    margin = serializers.FloatField()


class LogicSerializerRaw(serializers.Serializer):
    l_id = serializers.IntegerField()
    name = serializers.CharField()
    general_manager = serializers.CharField()
    contact_person = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.EmailField()
    pay_type = serializers.IntegerField()
    comment = serializers.CharField()


class CalcRaw(serializers.Serializer):
    loading_address = serializers.CharField()
    unloading_address = serializers.CharField()


class RequisitesSellerSerializerRaw(serializers.Serializer):
    rs_general_manager = serializers.CharField()
    rs_inn = serializers.CharField()
    rs_bank_name = serializers.CharField()
    rs_bic_bank = serializers.CharField()
    rs_cor_account = serializers.CharField()
    rs_customers_pay_account = serializers.CharField()
    rs_legal_address = serializers.CharField()
    rs_physical_address = serializers.CharField()


class RequisitesBuyerSerializerRaw(serializers.Serializer):
    rb_general_manager = serializers.CharField()
    rb_inn = serializers.CharField()
    rb_bank_name = serializers.CharField()
    rb_bic_bank = serializers.CharField()
    rb_cor_account = serializers.CharField()
    rb_customers_pay_account = serializers.CharField()
    rb_legal_address = serializers.CharField()
    rb_physical_address = serializers.CharField()
