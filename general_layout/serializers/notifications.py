from rest_framework import serializers

from general_layout.notifications.models.message_to_user import MessageToUser


class MessageToUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = MessageToUser
        fields = ['notification_to', 'current_deal', 'current_calculate', 'notification_message', 'created_date']
