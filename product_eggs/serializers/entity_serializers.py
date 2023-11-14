from rest_framework import serializers

from product_eggs.models.entity import EntityEggs


class EntityEggsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntityEggs
        fields = '__all__'
