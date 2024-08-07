import time
from django.http import StreamingHttpResponse, HttpResponse
from django_eventstream import send_event
from rest_framework.views import APIView
from rest_framework.response import Response
import logging
from rest_framework.renderers import JSONRenderer
from .sse_renderer import ServerSentEventRenderer
from .serializers.UserSerializer import CustomUserSerializer
import gevent
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)

class EventStreamView(APIView):
    renderer_classes = [ServerSentEventRenderer]

    def get(self, request, *args, **kwargs):
        response = StreamingHttpResponse(content_type='text/event-stream')
        response["X-Accel-Buffering"] = "no"  # Disable buffering in nginx
        response["Cache-Control"] = "no-cache"  # Ensure clients don't cache the data
        response['Transfer-Encoding'] = 'chunked'

        def event_generator():
            while True:
                yield f"data: Hello, this is a test message!\n\n"
                import time
                time.sleep(1)

        response.streaming_content = event_generator()
        return response

    def post(self, request, *args, **kwargs):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "events_group",
            {
                "type": "event_message",
                "message": request.data.get('message', 'No message')
            }
        )
        return Response(status=204)

    def event_generator(self, test):
        while True:
            # Example event generation logic
            yield f"{test}\n\n"
            gevent.sleep(1)
