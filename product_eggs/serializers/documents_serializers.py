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

