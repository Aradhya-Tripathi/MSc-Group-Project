from django.urls import path

from . import live


websocket_urlpatterns = [
    path("ws/signals", live.SignalsConsumer.as_asgi()),
]
