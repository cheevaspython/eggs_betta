from rest_framework import serializers


class FieldIsActiveOfferSerializer(serializers.Serializer):
    model_id = serializers.IntegerField()
    model_title = serializers.CharField()
