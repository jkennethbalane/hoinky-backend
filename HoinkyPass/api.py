from rest_framework.views import APIView
from .models import Quest
from .pagination import LimitOffsetPagination, get_paginated_response
from rest_framework import serializers, status
from rest_framework.response import Response
from .serializers.QuestSerializer import QuestSerializer
from .serializers.UserSerializer import CustomUserSerializer
from .selectors import get_quests, finished_quests, unfinished_quests, get_users, get_detail
from django.http import JsonResponse
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

class FinishedQuest(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10
        max_limit = 100

    def get(self, request, **kwargs):
        quest = finished_quests(user=request.user)
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=QuestSerializer,
            queryset=quest,
            request=request,
            view=self,
        )

class UnfinishedQuest(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10
        max_limit = 100

    def get(self, request, **kwargs):
        quest = unfinished_quests(user=request.user)
        
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=QuestSerializer,
            queryset=quest,
            request=request,
            view=self,
        )

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

class UserDetail(APIView):
    def get(self, request, qr, *args, **kwargs):
        user = get_detail(qr)
        serializer = CustomUserSerializer(user, context={'request': self.request})
        print(serializer.data)
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
        user.save()
        return Response({'status': 'success', 'message': 'User quests updated successfully'})
    