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

class SimpleQuestSerializer(serializers.ModelSerializer):
    is_finished = serializers.SerializerMethodField()

    class Meta:
        model = Quest
        fields = ['id', 'title', 'description', 'exp', 'is_finished']

    def get_is_finished(self, obj):
        user = self.context.get('user')
        if user and user.quests_achieved.filter(id=obj.id).exists():
            return True
        return False

class CustomUserSerializer(UserSerializer):
    quests = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = HoinkyUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'level', 'qr_unique', 'is_superuser', 'quests')

    def get_quests(self, obj):
        quests = Quest.objects.all()
        serializer = SimpleQuestSerializer(quests, many=True, context={'user': obj})
        return serializer.data

class CustomTokenCreateSerializer(TokenCreateSerializer):
    class Meta:
        fields = ('auth_token', 'is_superuser')

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data['is_superuser'] = user.is_superuser
        return data
