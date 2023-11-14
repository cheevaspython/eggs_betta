from dataclasses import dataclass
from typing import Type

from general_layout.bases.models.abstract_client_card import AbstractClientCard

from product_eggs.serializers.balance_serializers import StatisticClientSerializer


@dataclass(slots=True, frozen=True)
class SubscribeToRoom():
    """
    ModelsAndSerializers"""
    room_id: int
    room_name: str
    room_host: str
    add_message: str = "Вы добавлены в комнату чата"


@dataclass(slots=True, frozen=True)
class ModelsAndSerializers():
    model: Type[AbstractClientCard]
    serializer: Type[StatisticClientSerializer]

    def __getitem__(self, item):
        return getattr(self, item)
