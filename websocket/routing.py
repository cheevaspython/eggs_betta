from django.urls import path

from websocket.consumers.consumers_chat import ChatConsumer
from websocket.consumers.consumers_messages import MessageEggsSubConsumer
from websocket.consumers.consumers_side_bar import SideBarSubConsumer
from websocket.consumers.consumers_get_models import AllModelsSubConsumer
from websocket.consumers.consumers_balance import BalanceConsumer

websocket_urlpatterns = [
    path('ws/messageeggs_sub_consumer/', MessageEggsSubConsumer.as_asgi()),
    path('ws/left_side_bar/', SideBarSubConsumer.as_asgi()),
    path("ws/get_models/", AllModelsSubConsumer.as_asgi()),
    path("ws/balance/", BalanceConsumer.as_asgi()),
    path("ws/chat/", ChatConsumer.as_asgi()),
]
