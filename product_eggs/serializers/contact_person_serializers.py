from rest_framework import serializers

from product_eggs.models.contact_person import ContactPersonEggs


class ContactPersonEggsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactPersonEggs
        fields = '__all__'


class InnTypeClientSerializer(serializers.Serializer):
    client_inn = serializers.CharField()
    client_type = serializers.CharField()
