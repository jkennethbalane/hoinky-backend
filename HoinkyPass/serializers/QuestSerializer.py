from rest_framework import serializers
from ..models import Quest, HoinkyUser

class QuestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quest
        fields = ['id', 'title', 'description', 'exp']
    
class SimpleQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quest
        fields = "__all__"
        
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoinkyUser
        fields = "__all__"