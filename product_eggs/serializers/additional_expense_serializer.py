from rest_framework import serializers

from product_eggs.models.additional_expense import AdditionalExpenseEggs


class AdditionalExpenseEggsSerializer(serializers.Serializer):
    model_id = serializers.IntegerField()
    expense = serializers.FloatField()
    expense_detail_json_pre = serializers.JSONField()


class AdditionalExpenseEggsDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AdditionalExpenseEggs
        fields = '__all__'
