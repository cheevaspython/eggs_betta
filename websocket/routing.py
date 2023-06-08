from django.urls import path

from websocket.consumers.consumers_messages import MessageEggsSubConsumer
from websocket.consumers.consumers_side_bar import SideBarSubConsumer
from websocket.consumers.consumers import ModelSubConsumer
from websocket.consumers.consumers_mychat import RoomConsumer
from websocket.consumers.consumers_get_models import AllModelsSubConsumer
from websocket.consumers.consumers_balance import BalanceBuyerWs


websocket_urlpatterns = [
    path('ws/messageeggs_sub_consumer/', MessageEggsSubConsumer.as_asgi()),
    path('ws/left_side_bar/', SideBarSubConsumer.as_asgi()),
    path('ws/model_sub_consumer/', ModelSubConsumer.as_asgi()),
    path("ws/chat/", RoomConsumer.as_asgi()),
    path("ws/get_models/", AllModelsSubConsumer.as_asgi()),
    path("ws/balance_buyer/", BalanceBuyerWs.as_asgi()),
]
