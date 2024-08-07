import json
import time
from rest_framework.views import APIView
from .models import Quest
from django.db import models
from .pagination import LimitOffsetPagination, get_paginated_response
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers.QuestSerializer import QuestSerializer
from .serializers.UserSerializer import CustomUserSerializer
from .selectors import get_quests, finished_quests, unfinished_quests, get_users, get_detail
from django.http import JsonResponse, StreamingHttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404

@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

class QuestListAPIView(APIView):
    def get(self, request, **kwargs):
        quest = get_quests()
        serializer = QuestSerializer(quest, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, **kwargs):
        serializer = QuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class QuestEditAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, **kwargs):
        quest_id = kwargs.get('id', None)
        quest = get_object_or_404(Quest, id=quest_id)
        serializer = QuestSerializer(quest, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FinishedQuest(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10
        max_limit = 100

    def get(self, request, **kwargs):
        quest = finished_quests(user=request.user)
        print(quest)
        serializer = QuestSerializer(quest, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UnfinishedQuest(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10
        max_limit = 100

    def get(self, request, **kwargs):
        quest = unfinished_quests(user=request.user)
        print(quest)
        serializer = QuestSerializer(quest, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserList(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10
        max_limit = 100

    def get(self, request, **kwargs):
        user = get_users()
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=CustomUserSerializer,
            queryset=user,
            request=request,
            view=self,
        )

def calculate_level(exp):
        level_thresholds = {
            1: 0,
            2: 5,
            3: 15,
            4: 30,
        }
        for level, threshold in level_thresholds.items():
            if exp >= threshold:
                current_level = level
            else:
                break
        return current_level

class UserDetail(APIView):
    def get(self, request, qr, *args, **kwargs):
        user = get_detail(qr)
        serializer = CustomUserSerializer(user, context={'request': self.request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, qr, *args, **kwargs):
        user = get_detail(qr)
        toggle_ids = request.data.get('toggle', [])
        for item in toggle_ids:
            quest = get_object_or_404(Quest, id=item)
            if quest in user.quests_achieved.all():
                user.quests_achieved.remove(quest)
            else:
                user.quests_achieved.add(quest)
        total_exp = user.quests_achieved.aggregate(total=models.Sum('exp'))['total'] or 0
        level = calculate_level(total_exp)
        user.level = level
        user.save()
        return Response({'status': 'success', 'message': 'User quests updated successfully'})

class CurrentUser(APIView):
    def get(self, request):
        def event_stream():
            while True:
                user = request.user
                serializer = CustomUserSerializer(user)
                json_data = json.dumps(serializer.data)
                yield f"data: {json_data}\n\n"
                time.sleep(5)  # Adjust the interval as needed
        response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
        response['Cache-Control'] = 'no-cache'
        return response
    
    
    