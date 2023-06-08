import json
import logging

from channels.db import database_sync_to_async
from djangochannelsrestframework.observer.generics import \
    ObserverModelInstanceMixin, action, GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer

from websocket.middleware import get_model
from websocket.models import Room, Message, RoomSubscriber, SubscribeMessage
from websocket.serializers import MessageSerializer, MessageSubscriberSerializer, RoomSerializer
from users.serializers import CustomUserSerializer
from websocket.services.decorator import ws_auth
from users.models import CustomUser

logger = logging.getLogger(__name__)


class RoomConsumer(ObserverModelInstanceMixin, GenericAsyncAPIConsumer):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_field = "pk"
    auth = False
    user = None

    async def auth_close(self):
        await super().close() 

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

    @action()
    @ws_auth
    async def subscribe_to_await_subscribe(self, *args, **kwargs):
        await self.sub_message_activity.subscribe(roomsubscribe=1, user=self.user)

    @model_observer(SubscribeMessage)
    @ws_auth
    async def sub_message_activity(self, sub_message, observer=None, **kwargs):
        if sub_message['action'] == 'subscribe':
            await self.send_json(sub_message)

    @sub_message_activity.serializer
    def sub_message_activity_serializer(self, instance: Message, action, **kwargs):
        return dict(
            data=MessageSubscriberSerializer(instance).data,
            action='subscribe')

    @sub_message_activity.groups_for_signal
    def sub_message_activity(self, instance: SubscribeMessage, **kwargs):
        yield f'-user__{instance.user_id}'

    @sub_message_activity.groups_for_consumer
    def sub_message_activity(self, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-user__{kwargs["user"]}'

    @action()
    @ws_auth
    async def join_room(self, pk, **kwargs):
        self.room_subscribe = pk
        await self.add_user_to_room(pk)
        await self.send_json(
            {'data': await self.get_room_messages(pk),
             'action': 'get_room_messages'})
        await self.notify_users()

    async def disconnect(self, code):
        # if hasattr(self, "room_subscribe"):
            # await self.remove_user_from_room(self.room_subscribe)
            # await self.notify_users()
        await super().disconnect(code)

    @action()
    @ws_auth
    async def leave_room(self, pk, **kwargs) -> None:
        await self.remove_user_from_room(pk)

    @action()
    @ws_auth
    async def get_all_users(self, **kwargs):
        await self.send_json(
            {'data': await self.get_users(), 'action': 'get_all_users'})

    @action()
    @ws_auth
    async def create_room(self, room_name: str, room_users: list, **kwargs):
        await self.create_chat_room(room_name, set(room_users))

    @action()
    @ws_auth
    async def check_user_rooms(self, **kwargs):
        await self.send_json(
            {'data': await self.get_user_rooms(), 'action': 'check_user_rooms'})

    @database_sync_to_async
    def get_room_messages(self, pk: int):
        cur_room = Room.objects.get(pk=pk)
        return MessageSerializer(cur_room.messages.all(), many=True).data

    @database_sync_to_async
    def get_user_rooms(self) -> list:
        return [(room.pk, room.name,) for room in self.user.current_rooms.all()]

    @database_sync_to_async
    def get_users(self):
        return CustomUserSerializer(CustomUser.objects.all(), many=True).data

    @database_sync_to_async
    def create_message_db(self, room: Room, text: str) -> None:
        message = Message.objects.create(
                room=room,
                user=self.user,
                text=text,
        )
        message.save()

    @database_sync_to_async
    def create_chat_room(self, room_name: str, room_users: set) -> None:
        gen_usr_list = [CustomUser.objects.get(pk=cur_usr) for cur_usr in room_users]
        new_room = Room.objects.create(
                name=room_name,
                host=self.user,
        )
        for usr in gen_usr_list:
            new_room.current_users.add(usr)
        new_room.save()
        for user in gen_usr_list:
            sub_message = SubscribeMessage.objects.create(
                room=RoomSubscriber.objects.get(pk=1),
                user=user,
                sub_text=RoomSerializer(new_room).data,
            )
            sub_message.save()

    @action()
    @ws_auth
    async def create_message(self, message, **kwargs):
        room: Room = await self.get_room(pk=self.room_subscribe)
        await self.create_message_db(room, message)

    @action()
    @ws_auth
    async def subscribe_to_messages_in_room(self, *args, **kwargs):
        await self.message_activity.subscribe(room=kwargs['pk'])

    @model_observer(Message)
    @ws_auth
    async def message_activity(self, message, observer=None, **kwargs):
        if message['action'] == 'create':
            await self.send_json(message)

    @message_activity.serializer
    def message_activity_serializer(self, instance: Message, action, **kwargs):
        return dict(
            data=MessageSerializer(instance).data,
            action=action.value)

    @message_activity.groups_for_signal
    def message_activity(self, instance: Message, **kwargs):
        yield f'room__{instance.room.pk}'
        yield f'pk__{instance.pk}'

    @message_activity.groups_for_consumer
    def message_activity(self, room=None, **kwargs):
        if room:
            yield f'room__{room}'

    async def notify_users(self):
        room: Room = await self.get_room(self.room_subscribe)
        for group in self.groups:
            await self.channel_layer.group_send(
                group,
                {
                    'type': 'update_users',
                    'members': await self.current_users(room)
                }
            )

    async def update_users(self, event: dict):
        await self.send(text_data=json.dumps({'members': event["members"]}))

    @database_sync_to_async
    def get_room(self, pk: int) -> Room:
        return Room.objects.get(pk=pk)

    @database_sync_to_async
    def current_users(self, room: Room):
        return [CustomUserSerializer(user).data for user in room.current_users.all()]

    @database_sync_to_async
    def remove_user_from_room(self, room_id):
        self.user.current_rooms.remove(room_id)

    @database_sync_to_async
    def add_user_to_room(self, pk):
        if not self.user.current_rooms.filter(pk=self.room_subscribe).exists():
            self.user.current_rooms.add(Room.objects.get(pk=pk))
        else:
            pass

    async def send_json(self, content, close=False):
        """
        Custom send, for change dumps, for rus latters.
        """
        await super().send(text_data=await self.encode_json(content), close=close)

    async def encode_json(self, content):
        return json.dumps(content, ensure_ascii=False)

    async def check_action(self, message: str, action: str, request_id: str):
        allow_methhods = ('delete', 'create')
        if action in allow_methhods:
            await self.reply(data=message, action=action, request_id=request_id)
