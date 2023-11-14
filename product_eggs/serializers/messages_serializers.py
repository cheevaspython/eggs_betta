from rest_framework import serializers

from product_eggs.models.messages import MessageToUserEggs


class MessageToUserEggsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUserEggs
        fields = [
            'id', 'message_to', 'current_base_deal', 'message',
            'not_read', 'current_seller', 'created_date',
            'current_buyer', 'current_logic', 'current_app_seller',
            'current_app_buyer', 'done', 'info',
        ]

