from rest_framework import serializers

from product_eggs.models.documents import DocumentsDealEggsModel, DocumentsContractEggsModel, \
    DocumentsBuyerEggsModel


class DocumentsDealEggsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DocumentsDealEggsModel
        fields = '__all__' 


class DocumentsContractEggsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DocumentsContractEggsModel
        fields = '__all__'


class DocumentsBuyerSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentsBuyerEggsModel
        fields = '__all__'


class DocumentsDealGetEggsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DocumentsDealEggsModel
        fields = [
            'id', 'payment_for_contract', 'payment_order_incoming', 'payment_order_outcoming',
            'specification_seller', 'account_to_seller', 'account_to_seller', 'account_to_buyer', 
            'application_contract_logic', 'account_to_logic', 'UPD_incoming', 'account_invoicing_from_seller',
            'product_invoice_from_seller', 'UPD_outgoing', 'account_invoicing_from_buyer', 
            'product_invoice_from_buyer', 'veterinary_certificate_buyer', 'veterinary_certificate_seller',
            'international_deal_CMR', 'international_deal_TTN', 'UPD_logic', 'account_invoicing_logic', 
            'product_invoice_logic',
        ]
