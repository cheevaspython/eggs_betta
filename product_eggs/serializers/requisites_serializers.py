from rest_framework import serializers

from product_eggs.models.requisites import RequisitesEggs


class RequisitesEggsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = RequisitesEggs
        fields = '__all__'


class RequisitesSerializer(serializers.Serializer):
    general_manager = serializers.CharField()
    inn = serializers.CharField()
    kpp = serializers.CharField()
    bank_name = serializers.CharField()
    bic_bank = serializers.CharField()
    cor_account = serializers.CharField()
    customers_pay_account = serializers.CharField()
    legal_address = serializers.CharField()
    physical_address = serializers.CharField()
    mail_address = serializers.CharField()
    register_date = serializers.CharField()
    name=serializers.CharField(),
    country=serializers.CharField(),
    region=serializers.CharField(),
    city=serializers.CharField(),
    email=serializers.CharField(),
    site=serializers.CharField(),
    phone=serializers.CharField(),
    phone2=serializers.CharField(),
    phone_with_out_code=serializers.CharField(),


