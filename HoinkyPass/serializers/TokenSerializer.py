from djoser.serializers import TokenCreateSerializer, TokenSerializer
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework import serializers

class CustomTokenCreateSerializer(TokenCreateSerializer):
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        fields = ('auth_token', 'is_superuser', 'user')  # Add other necessary fields manually

    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_superuser'] = self.user.is_superuser
        return data