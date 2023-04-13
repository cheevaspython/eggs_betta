from rest_framework import serializers

from product_eggs.models.additional_expense import AdditionalExpenseEggs


class AdditionalExpenseSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AdditionalExpenseEggs
        fields = '__all__'
