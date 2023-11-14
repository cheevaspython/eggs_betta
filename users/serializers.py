from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'first_name', 'last_name', 'email', 'master_password']


class CheckMasterPasswordSerializer(serializers.Serializer):
    entered_password = serializers.CharField()


class CustomUserSerializerWs(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'first_name', 'last_name', ]
