from django.contrib import admin

from websocket.models import Room, Message, \
    RoomSubscriber, SubscribeMessage

admin.site.register(
        [
            Room, Message, RoomSubscriber, 
            SubscribeMessage
        ]
)
