import logging

from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action
from channels.db import database_sync_to_async

from product_eggs.models.messages import MessageToUserEggs
from product_eggs.serializers.messages_serializers import MessageToUserEggsSerializer
from users.serializers import CustomUserSerializer
from users.models import CustomUser
from websocket.consumers.consumers import CustomAPIConsumer

logger = logging.getLogger(__name__)


class MessageEggsSubConsumer(CustomAPIConsumer):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @action()
    async def get_active_messages(self, action: str, **kwargs):
        if self.auth:
            await self.reply(
                data=await self.get_current_messages(), action=action)
        else:
            await super().close()

    @model_observer(MessageToUserEggs, serializer_class=MessageToUserEggsSerializer)
    async def message_eggs_activity(
            self, message: str, action: str, subscribing_request_ids=[], **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.reply(data=message, action=action, request_id=request_id)
        else:
            await super().close()

    @message_eggs_activity.groups_for_signal
    def message_eggs_activity(self, instance: MessageToUserEggs, **kwargs):
        yield f'-message_to__{instance.message_to_id}'

    @message_eggs_activity.groups_for_consumer
    def message_eggs_activity(self, school=None, classroom=None, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-message_to__{kwargs["user"].pk}'

    @action()
    async def subscribe_to_message_eggs(self, request_id: str, **kwargs):
        if self.auth:
            await self.message_eggs_activity.subscribe(
                request_id=request_id, user=self.user)
        else:
            await super().close()

    @database_sync_to_async
    def get_current_messages(self) -> dict | None:
        if self.auth:
            messages = MessageToUserEggsSerializer(
                MessageToUserEggs.objects.filter(is_active=True, message_to=self.user),
                many=True)
            return messages.data

