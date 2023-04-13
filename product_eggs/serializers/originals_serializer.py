from rest_framework import serializers

from product_eggs.models.origins import OriginsDealEggs


class OriginsDealEggsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OriginsDealEggs
        fields = '__all__'
