from rest_framework import serializers

from product_eggs.models.tails import TailsContragentModelEggs


class TailsEggsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TailsContragentModelEggs
        fields = '__all__'
