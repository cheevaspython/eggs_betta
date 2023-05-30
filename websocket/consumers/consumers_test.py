import json
import logging

from channels.db import database_sync_to_async
from djangochannelsrestframework.observer.generics import \
    ObserverModelInstanceMixin, action, GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer

from websocket.models import Room, Message
from websocket.serializers import MessageSerializer, RoomSerializer
from websocket.middleware import get_model
from users.serializers import CustomUserSerializer
from users.models import CustomUser

logger = logging.getLogger(__name__)


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"
    auth = False

    @action()
    async def authorization(self, request_id: str, action: str, **kwargs):
        if kwargs['token']:
            try:
                self.user = await get_model(kwargs['token'])
                if self.user:
                    self.auth = True
                    await self.reply(
                        data={'authorization': True, 'user': self.user.pk}, action=action)
            except AttributeError as e:
                logger.info('wrong token in ws auth', e)

    async def disconnect(self, code): #TODO code?
        if hasattr(self, "room_subscribe"):
            await self.remove_user_from_room(self.room_subscribe)
            await self.notify_users()
        await super().disconnect(code)

    @action()
    async def join_room(self, pk: int, **kwargs):
        if self.auth:
            self.room_subscribe = pk
            await self.add_user_to_room(pk)
            await self.notify_users()
        else:
            await super().close() 

    @action()
    async def leave_room(self, pk: int, **kwargs):
        await self.remove_user_from_room(pk)

    @action()
    async def create_message(self, message: str, **kwargs):
        if self.auth:
            room: Room = await self.get_room(pk=self.room_subscribe)
            await database_sync_to_async(Message.objects.create)(
                room=room,
                user=self.user,
                text=message)
        else:
            await super().close() 

    @action()
    async def subscribe_to_messages_in_room(self, request_id: str, pk: int, **kwargs):
        if self.auth:
            await self.message_activity.subscribe(
                    request_id=request_id, room=pk, user=self.user)
        else:
            await super().close() 

    @model_observer(Message, serializer=MessageSerializer)
    async def message_activity(
            self, message: str, action: str, subscribing_request_ids=[], observer=None, **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.reply(
                    data=await self.get_message(message['pk']),
                    action=action,
                    request_id=request_id
                )
        else:
            await super().close() 

    @message_activity.groups_for_signal
    def message_activity_group(self, instance: Message, **kwargs):
        yield f'room__{instance.room.pk}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room is not None:
            yield f'room__{room}'

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'users': await self.current_users(room)
                }
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'users': event["users"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> Room:
        if self.auth:
            return Room.objects.get(pk=pk)

    @database_sync_to_async
    def get_message(self, pk: int) -> dict | None:
        if self.auth:
            instance = Message.objects.get(pk=pk)
            return_dict = {
                'message': instance.pk,
                'text': instance.text,
            }
            return return_dict 

    @database_sync_to_async
    def current_users(self, room: Room):
        if self.auth:
            return [
                CustomUserSerializer(user).data for user in room.current_users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room: Room):
        if self.auth:
            self.user.current_rooms.remove(room)

    @database_sync_to_async
    def add_user_to_room(self, pk: int):
        if self.auth:
            if not self.user.current_rooms.filter(pk=self.room_subscribe).exists():
                self.user.current_rooms.add(Room.objects.get(pk=pk))
