from django.utils import timezone
from rest_framework import serializers

from users.serializers import CustomUserSerializerWs
from websocket.models import CustomRoom, WsMessage, GeneralRoom, GeneralWsMessage

tz = timezone.get_default_timezone()


class MessageWsSerializer(serializers.ModelSerializer):
    friendly_date = serializers.SerializerMethodField()
    username = serializers.ReadOnlyField(source='username_orm')

    def get_friendly_date(self, instance):
        return instance.created_at.astimezone(tz).strftime("%H:%M:%S - %b %d %Y")

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

    def get_users_names(self, instance):
        cur_model = CustomRoom.objects.filter(pk=instance.pk).select_related(
                'host', 'zakrep_model'
            ).prefetch_related(
                'current_users'
            ).first()
        if cur_model:
            serializer = CustomUserSerializerWs(
                cur_model.current_users.all(), many=True
            )
            return serializer.data

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






