from rest_framework import serializers

from product_eggs.models.documents import DocumentsContractEggsModel


class StatisticBuyerClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DocumentsContractEggsModel
        fields = '__all__'

    name = serializers.CharField() 
    inn = serializers.IntegerField() 
    general_manager = serializers.CharField() 
    phone = serializers.CharField()
    email = serializers.EmailField()
    pay_type = serializers.IntegerField() 
    contact_person = serializers.CharField()
    comment = serializers.CharField()
    manager_id = serializers.IntegerField()
    documents_contract_id = serializers.CharField()

    tails_id = serializers.CharField()

    pay_limit = serializers.FloatField() 
    pay_limit_cash = serializers.FloatField() 

    balance = serializers.FloatField()
    balance_form_one = serializers.FloatField()
    balance_form_two = serializers.FloatField()

    general_manager = serializers.CharField()
    inn = serializers.CharField()
    bank_name = serializers.CharField()
    bic_bank = serializers.CharField()
    cor_account = serializers.CharField()
    customers_pay_account = serializers.CharField()
    legal_address = serializers.CharField()
    physical_address = serializers.CharField()


class StatisticSellerClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DocumentsContractEggsModel
        fields = '__all__'

    name = serializers.CharField() 
    inn = serializers.IntegerField() 
    general_manager = serializers.CharField() 
    phone = serializers.CharField()
    email = serializers.EmailField()
    pay_type = serializers.IntegerField() 
    contact_person = serializers.CharField()
    comment = serializers.CharField()
    manager_id = serializers.IntegerField()
    documents_contract_id = serializers.CharField()

    tails_id = serializers.CharField()

    balance = serializers.FloatField()
    balance_form_one = serializers.FloatField()
    balance_form_two = serializers.FloatField()

    general_manager = serializers.CharField()
    inn = serializers.CharField()
    bank_name = serializers.CharField()
    bic_bank = serializers.CharField()
    cor_account = serializers.CharField()
    customers_pay_account = serializers.CharField()
    legal_address = serializers.CharField()
    physical_address = serializers.CharField()
