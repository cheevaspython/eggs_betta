from rest_framework import serializers

from product_eggs.models.message_to_user_eggs import MessageToUserEggs


class MessageToUserEggsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUserEggs
        fields = [
            'id', 'notification_to', 'current_deal', 'current_calculate', 'current_conf_calculate', 
            'notification_message', 'not_read', 'created_date', 'current_seller', 
            'current_buyer', 'current_logic',
        ]

