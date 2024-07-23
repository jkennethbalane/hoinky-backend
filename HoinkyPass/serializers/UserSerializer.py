from djoser.serializers import UserCreateSerializer, UserSerializer, TokenCreateSerializer
from rest_framework import serializers
from ..models import Quest, HoinkyUser
from .QuestSerializer import QuestSerializer

class CustomUserCreateSerializer(UserCreateSerializer):
    def create(self, validated_data):
        if not validated_data.get('first_name'):
            raise serializers.ValidationError("First name is required.")
        return super().create(validated_data)

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'level')

class CustomUserSerializer(UserSerializer):
    quest_achieved = QuestSerializer(many=True, read_only=True)

    class Meta(UserSerializer.Meta):
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'level', 'quest_achieved', 'qr_unique', 'is_superuser')

class CustomTokenCreateSerializer(TokenCreateSerializer):
    class Meta:
        fields = ('auth_token', 'is_superuser')

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['is_superuser'] = user.is_superuser
        return data
