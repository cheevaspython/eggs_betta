import json 

from django.contrib.auth import get_user_model
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action
from channels.db import database_sync_to_async

from product_eggs.models.messages import MessageToUserEggs
from product_eggs.serializers.messages_serializers import MessageToUserEggsSerializer
from users.serializers import CustomUserSerializer 
from users.models import CustomUser
from websocket.middleware import get_model

User = get_user_model()


class MessageEggsSubConsumer(GenericAsyncAPIConsumer):
    queryset = CustomUser.objects.all() 
    serializer_class = CustomUserSerializer
    auth = False
    user = None

    @action()
    async def authorization(self, request_id: str, action: str, **kwargs):
        if kwargs['token']:
            self.user = await get_model(kwargs['token'])
            if self.user:
                self.auth = True
                await self.reply(
                    data={'authorization': True, 'user': self.user.pk}, action=action)

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

    async def encode_json(self, content):
        return json.dumps(content, ensure_ascii=False)

    async def check_action(self, message: str, action: str, request_id: str):
        allow_methhods = ('delete', 'create', 'update')
        if action in allow_methhods:
            await self.reply(data=message, action=action, request_id=request_id)
