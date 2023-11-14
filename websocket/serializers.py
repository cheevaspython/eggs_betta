from django.utils import timezone

from rest_framework import serializers

from websocket.models import CustomRoom, WsMessage, GeneralRoom, GeneralWsMessage

tz = timezone.get_default_timezone()


class MessageWsSerializer(serializers.ModelSerializer):
    friendly_date = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_friendly_date(self, instance):
        return instance.created_at.astimezone(tz).strftime("%H:%M:%S - %b %d %Y")

    def get_username(self, instance):
        return instance.user.username

    class Meta:
        model = WsMessage
        # exclude = []
        fields = [
            'pk', 'room', 'text',
            'is_active', 'created_at',
            'friendly_date', 'username'
        ]


class CustomRoomSerializer(serializers.ModelSerializer):
    users_names = serializers.SerializerMethodField()

    def get_users_names(self, instance) -> list[str]:
        return_username_list = list()
        for user in instance.current_users.all():
            return_username_list.append([user.username, user.first_name, user.last_name, user.id, user.role])
        return return_username_list

    class Meta:
        model = CustomRoom
        fields = [
            'pk', 'name', 'host',
            'current_users',
            'zakrep', 'zakrep_model',
            'users_names',
        ]


class GeneralRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralRoom
        fields = '__all__'


class GeneralMessageWsSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeneralWsMessage
        fields = '__all__'






