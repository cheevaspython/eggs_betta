from django.contrib import admin

from websocket.models import CustomRoom, GeneralWsMessage, \
    WsMessage, GeneralRoom

admin.site.register(
        [
            GeneralRoom, WsMessage,
            CustomRoom, GeneralWsMessage,
        ]
)
