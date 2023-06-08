from rest_framework import serializers

from websocket.models import Room, Message, RoomSubscriber, SubscribeMessage


class MessageSerializer(serializers.ModelSerializer):
    # created_at_formatted = serializers.SerializerMethodField()
    # user = CustomUserSerializer()
    friendly_date = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_friendly_date(self, instance):
        return instance.created_at.strftime("%H:%M:%S - %b %d %Y")

    def get_username(self, instance):
        return instance.user.username

    class Meta:
        model = Message
        # exclude = []
        fields = ['pk', 'room', 'text', 'is_active', 'created_at', 'friendly_date', 'username']


class RoomSerializer(serializers.ModelSerializer):
    # last_message = serializers.SerializerMethodField()
    # messages = MessageSerializer(source='messages',many=True, read_only=True)

    # def get_last_message(self, instance):
    #     return MessageSerializer(instance.messages.order_by('created_at').last(10)).data

    class Meta:
        model = Room
        fields = [
            'pk', 'name', 'host', 
            'current_users',# 'last_message'
        ]
        # depth = 1
        # read_only_fields = ["messages", "last_message"]


class RoomSubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomSubscriber
        fields = '__all__'


class MessageSubscriberSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubscribeMessage
        fields = '__all__'






