from rest_framework import serializers


class RequisitesSerializer(serializers.Serializer):

    general_manager = serializers.CharField()
    inn = serializers.CharField()
    bank_name = serializers.CharField()
    bic_bank = serializers.CharField()
    cor_account = serializers.CharField()
    customers_pay_account = serializers.CharField()
    legal_address = serializers.CharField()
    physical_address = serializers.CharField()


