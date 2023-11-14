import logging

from channels.db import database_sync_to_async

from djangochannelsrestframework.observer.generics import action
from djangochannelsrestframework.observer import model_observer

from rest_framework.serializers import ReturnDict
from product_eggs.models.base_deal import BaseDealEggsModel

from websocket.consumers.consumers import CustomAPIConsumer
from websocket.models import CustomRoom, WsMessage, GeneralRoom, GeneralWsMessage
from websocket.serializers import (
    GeneralMessageWsSerializer, MessageWsSerializer, CustomRoomSerializer
)
from websocket.services.decorator import ws_auth

from users.models import CustomUser
from users.serializers import CustomUserSerializerWs

logger = logging.getLogger(__name__)


class ChatConsumer(CustomAPIConsumer):
    queryset = CustomRoom.objects.all()
    serializer_class = CustomRoomSerializer
    lookup_field = 'pk'
    current_active_rooms: set = set()
    general_room = GeneralRoom.objects.get_or_create(pk=1)

    @action()
    @ws_auth
    async def get_all_users(self, action, *args, **kwargs):
        await self.reply(data=await self.get_users_from_db(), action=action)

    @action()
    @ws_auth
    async def create_chat_room(
            self, room_name: str,
            users_list: list,
            action: str,
            text_room: str | None = None,
            model_id: int | None = None,
            **kwargs):
        room_data = await self.room_creator(room_name, users_list, text_room, model_id)
        await self.reply(data=room_data, action=action)
        for user_pk in room_data['current_users']:
            await self.create_general_message(
                user_pk,
                {'host': [self.user.pk, self.user.username],
                'add_to_room': room_data['pk']}
            )
            await self.reconnect_subscribe_all_user_rooms()

    @action()
    @ws_auth
    async def reconnect_subscribe_all_user_rooms(self, *args, **kwargs) -> None:
        user_rooms: set = await self.get_user_active_rooms()
        need_to_connect: set = user_rooms - self.current_active_rooms
        need_to_disconnect: set = self.current_active_rooms - user_rooms
        await self.subscribe_to_gen_messages()
        if need_to_connect or need_to_disconnect:
            self.current_active_rooms = self.current_active_rooms | need_to_connect
            [await self.subscribe_to_messages_current_room(pk=room_pk) for room_pk in need_to_connect]
            room_message_data = [await self.get_room_messages(room_pk) for room_pk in user_rooms]
            await self.send_json({'data': room_message_data, 'action': 'connected to rooms'})

    @action()
    @ws_auth
    async def add_user_to_room(self, room_pk: int, user_pk_list: list[int], action: str, *args, **kwargs):
        if user_pk_list:
            for user_pk in user_pk_list:
                room_data: ReturnDict = await self.add_user_to_room_db(room_pk, user_pk)
                if room_data and self.user:
                    await self.reply(data=room_data, action=action)
                    await self.create_general_message(
                        user_pk,
                        {'host': [self.user.pk, self.user.username],
                        'add_to_room': room_pk}
                    )
                    await self.reconnect_subscribe_all_user_rooms()
                else:
                    await self.reply(data='permission denied or user already in room', action=action)

    @action()
    @ws_auth
    async def delete_room(self, room_pk: int, action, *args, **kwargs):
        room_delete_data = await self.room_deleter(room_pk)
        await self.reply(data=room_delete_data, action=action)
        for user_pk in room_delete_data['current_users']:
            if self.user:
                await self.create_general_message(
                    user_pk,
                    {'host': [self.user.pk, self.user.username],
                    'delete_for_room': room_delete_data['pk']}
                )

    @action()
    @ws_auth
    async def create_message(self, message: str, action: str, room_pk: int, **kwargs):
        room: CustomRoom = await self.get_room(pk=room_pk)
        await self.create_message_db(room, message)

    @action()
    @ws_auth
    async def create_general_message(
            self, add_user_pk: int,
            json_data: dict, **kwargs):
        await self.reply(
            data=await self.create_gen_message_db(add_user_pk, json_data),
            action='create',
        )

    @action()
    @ws_auth
    async def subscribe_to_messages_current_room(self, *args, **kwargs) -> None:
        if kwargs['pk']:
            await self.room_messages_activity.subscribe(room=kwargs['pk'])

    @action()
    @ws_auth
    async def subscribe_to_gen_messages(self, *args, **kwargs) -> None:
        await self.check_add_to_generalroom()
        await self.gen_room_messages_activity.subscribe(user=self.user)

    #подписка на сообщения конкретной комнаты
    @model_observer(WsMessage)
    @ws_auth
    async def room_messages_activity(self, message: dict, observer=None, **kwargs):
        if message['action'] == 'create':
            await self.reply(
                data=message['data'],
                action='create_message',
            )

    @room_messages_activity.serializer
    def message_activity_serializer(self, instance: WsMessage, action, **kwargs):
        return dict(
            data=MessageWsSerializer(instance).data,
            action=action.value)

    @room_messages_activity.groups_for_consumer
    def room_messages_activity(self, room=None, **kwargs):
        if room:
            yield f'room__{room}'

    @room_messages_activity.groups_for_signal
    def room_messages_activity(self, instance: WsMessage, **kwargs):
        yield f'room__{instance.room.pk}'
        yield f'pk__{instance.pk}'

    #подписка на сообщения общей комнаты
    @model_observer(GeneralWsMessage)
    @ws_auth
    async def gen_room_messages_activity(self, gen_message, observer=None, **kwargs):
        if gen_message['action'] == 'create':
            await self.send_json(gen_message)
            await self.reconnect_subscribe_all_user_rooms()

    @gen_room_messages_activity.serializer
    def gen_message_activity_serializer(self, instance: GeneralWsMessage, action, **kwargs):
        return dict(
            data=GeneralMessageWsSerializer(instance).data,
            action=action.value)

    @gen_room_messages_activity.groups_for_signal
    def gen_room_messages_activity(self, instance: GeneralWsMessage, **kwargs):
        yield f'gen_room__{instance.gen_room.pk}'
        yield f'-to_user__{instance.to_user_id}'

    @gen_room_messages_activity.groups_for_consumer
    def gen_room_messages_activity(self, room=None, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-to_user__{kwargs["user"].pk}'

    @database_sync_to_async
    def customuser_converter(self, cur_users: list[int]) -> list[CustomUser]:
        return [CustomUser.objects.get(pk=cur_pk) for cur_pk in cur_users]

    @database_sync_to_async
    def get_users_from_db(self) -> ReturnDict:
        return CustomUserSerializerWs(CustomUser.objects.all(), many=True).data

    @database_sync_to_async
    def room_deleter(self, room_pk: int) -> ReturnDict | str:
        room: CustomRoom = CustomRoom.objects.get(pk=room_pk)
        if room.host == self.user:
            room.is_active = False
            room.save()
            return CustomRoomSerializer(room).data
        else:
            return 'you cant delete this room, permission denied.'

    @database_sync_to_async
    def room_creator(self,
            room_name: str,
            users_list: list[int],
            text_room: str | None,
            model_id: int | None
            ) -> ReturnDict:
        if model_id:
            cur_model = BaseDealEggsModel.objects.get(pk=model_id)
        else:
            cur_model = None
        new_room = CustomRoom.objects.create(
            name = room_name,
            host = self.user,
            zakrep = text_room,
            zakrep_model = cur_model,
        )
        for user in [CustomUser.objects.get(pk=cur_pk) for cur_pk in users_list]:
            new_room.current_users.add(user)
        new_room.save()
        return CustomRoomSerializer(new_room).data

    @database_sync_to_async
    def get_user_active_rooms(self) -> set[int] | set:
        active_rooms = CustomUser.objects.get(pk=self.user.pk).current_rooms.filter(is_active=True)
        host_rooms = CustomUser.objects.get(pk=self.user.pk).host_rooms.filter(is_active=True)
        user_rooms = set(room.pk for room in active_rooms) | set(room.pk for room in host_rooms)
        return user_rooms if user_rooms else set()

    @database_sync_to_async
    def add_user_to_room_db(self, room_pk: int, user_pk: int) -> ReturnDict | None:
        current_room = CustomRoom.objects.get(pk=room_pk)
        if current_room.host == self.user:
            add_user = CustomUser.objects.get(pk=user_pk)
            if add_user not in current_room.current_users.all():
                current_room.current_users.add(add_user)
                current_room.save()
                return CustomRoomSerializer(current_room).data
            else:
                return None
        else:
            return None

    @database_sync_to_async
    def create_message_db(self, room: CustomRoom, text: str) -> ReturnDict:
        message = WsMessage.objects.create(
            room=room,
            user=self.user,
            room_cur_users=str(room.current_users),
            text=text,
        )
        message.save()
        return MessageWsSerializer(message).data

    @database_sync_to_async
    def create_gen_message_db(self, add_user_pk: int, json_data: dict) -> ReturnDict:
        gen_message = GeneralWsMessage.objects.create(
            gen_room=self.general_room[0],
            to_user=CustomUser.objects.get(pk=add_user_pk),
            sub_text=json_data,
        )
        gen_message.save()
        return GeneralMessageWsSerializer(gen_message).data

    @database_sync_to_async
    def get_room(self, pk: int) -> CustomRoom:
        return CustomRoom.objects.get(pk=pk)

    @database_sync_to_async
    def get_room_messages(self, pk: int) -> dict:
        cur_room = CustomRoom.objects.get(pk=pk)
        return {
            'room_details': CustomRoomSerializer(cur_room).data,
            'room_messages': MessageWsSerializer(cur_room.messages.all(), many=True).data
        }

    @database_sync_to_async
    def check_add_to_generalroom(self) -> None:
        if self.user not in self.general_room[0].current_users.all():
            self.general_room[0].current_users.add(self.user)
            self.general_room[0].save()



