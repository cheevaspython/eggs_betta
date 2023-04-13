from rest_framework import serializers

from product_eggs.models.messages import MessageToUserEggs


class MessageToUserEggsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUserEggs
        fields = [
            'id', 'message_to', 'current_base_deal', 'message',
            'not_read', 'created_date', 'current_seller', 
            'current_buyer', 'current_logic',
        ]

