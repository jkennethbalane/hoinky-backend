from rest_framework.views import APIView
from .models import Quest

from .pagination import LimitOffsetPagination, get_paginated_response
from rest_framework import serializers, status
from rest_framework.response import Response
from .serializers.QuestSerializer import QuestSerializer
from .serializers.UserSerializer import CustomUserSerializer
from .selectors import get_quests, finished_quests, unfinished_quests, get_users, get_detail

class QuestListAPIView(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10
        max_limit = 100

    def get(self, request, **kwargs):
        quest = get_quests()
        
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=QuestSerializer,
            queryset=quest,
            request=request,
            view=self,
        )
    
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
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)