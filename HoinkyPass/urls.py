from . import api
from django.urls import path
from .views import EventStreamView

urlpatterns = [
    path("quests/", api.QuestListAPIView.as_view(), name="quests"),
    path("quests/finished/", api.FinishedQuest.as_view(), name="finished_quest"),
    path("quests/unfinished/", api.UnfinishedQuest.as_view(), name="unfinished_quest"),
    path("quests/<str:id>/", api.QuestEditAPIView.as_view(), name="edit_quests"),
    path("user", api.UserList.as_view(), name="user_list"),
    path("user/sse/", api.CurrentUser.as_view(), name="user_list"),
    path("user/<str:qr>/", api.UserDetail.as_view(), name='user_detail'),
    path('get-csrf-token/', api.get_csrf_token, name='get_csrf_token'),
    path('events/', EventStreamView.as_view(), name='event-stream'),
]