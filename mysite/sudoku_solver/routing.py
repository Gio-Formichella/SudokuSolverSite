from django.urls import re_path
from .consumers import BoardConsumer

websocket_urlpatterns = [
    re_path("ws/board/", BoardConsumer.as_asgi()),
]
