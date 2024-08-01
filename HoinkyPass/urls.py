from . import api
from django.urls import path

urlpatterns = [
    path("quests/", api.QuestListAPIView.as_view(), name="quests"),
    path("quests/finished/", api.FinishedQuest.as_view(), name="finished_quest"),
    path("quests/unfinished/", api.UnfinishedQuest.as_view(), name="unfinished_quest"),
    path("user", api.UserList.as_view(), name="user_list"),
    path("user/<str:qr>/", api.UserDetail.as_view(), name='user_detail'),
    path('get-csrf-token/', api.get_csrf_token, name='get_csrf_token'),
]