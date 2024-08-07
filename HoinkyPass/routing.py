from django.urls import path, re_path
from HoinkyPass.consumers import RealTimeConsumer

websocket_urlpatterns = [
    re_path(r'^ws/some_path/$', RealTimeConsumer.as_asgi()),
]