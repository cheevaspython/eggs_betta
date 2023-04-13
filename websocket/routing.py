from django.urls import path, re_path

from websocket import consumers


websocket_urlpatterns = [
    path("ws/", consumers.UserConsumer.as_asgi()),
    path('ws/chat/', consumers.RoomConsumer.as_asgi()),
]
