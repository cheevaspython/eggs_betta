import json 

from django.db.models import Prefetch
from django.db.models import Q
from django.contrib.auth import get_user_model
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action
from channels.db import database_sync_to_async

from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.balance_serializers import StatisticBuyerClientSerializer, \
    StatisticLogicClientSerializer, StatisticSellerClientSerializer
from users.serializers import CustomUserSerializer 
from users.models import CustomUser
from websocket.middleware import get_model

User = get_user_model()


class BalanceBuyerWs(GenericAsyncAPIConsumer):
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

    @model_observer(BuyerCardEggs)
    async def balance_buyer_activity(
            self, message: str, action: str, subscribing_request_ids=[], **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.reply(data=await self.get_list_buyer(), action=action, request_id=request_id)
        else:
            await super().close() 

    @model_observer(LogicCardEggs)
    async def balance_logic_activity(
            self, message: str, action: str, subscribing_request_ids=[], **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.reply(data=await self.get_list_logic(), action=action, request_id=request_id)
        else:
            await super().close() 

    @model_observer(SellerCardEggs)
    async def balance_seller_activity(
            self, message: str, action: str, subscribing_request_ids=[], **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.reply(data=await self.get_list_seller(), action=action, request_id=request_id)
        else:
            await super().close() 

    @balance_buyer_activity.serializer
    def balance_buyer_activity(self, instance: BuyerCardEggs, action, **kwargs):
        if instance.balance:
            return StatisticBuyerClientSerializer(instance).data
        else:
            pass

    @balance_logic_activity.serializer
    def balance_logic_activity(self, instance: LogicCardEggs, action, **kwargs):
        if instance.balance:
            return StatisticLogicClientSerializer(instance).data
        else:
            pass

    @balance_buyer_activity.serializer
    def balance_seller_activity(self, instance: SellerCardEggs, action, **kwargs):
        if instance.balance:
            return StatisticSellerClientSerializer(instance).data
        else:
            pass

    @action()
    async def subscribe_to_balance(self, request_id: str, **kwargs):
        if self.auth:
            await self.balance_buyer_activity.subscribe(
                request_id=request_id)
            await self.balance_seller_activity.subscribe(
                request_id=request_id)
            await self.balance_logic_activity.subscribe(
                request_id=request_id)
        else:
            await super().close() 

    @action()
    async def get_balance_buyer(self, action: str, **kwargs):
        if self.auth:
            await self.reply(
                data=await self.get_list_buyer(),
                action=action,
            )
        else:
            await super().close() 

    @action()
    async def get_balance_seller(self, action: str, **kwargs):
        if self.auth:
            await self.reply(
                data=await self.get_list_seller(),
                action=action,
            )
        else:
            await super().close() 

    @action()
    async def get_balance_logic(self, action: str, **kwargs):
        if self.auth:
            await self.reply(
                data=await self.get_list_logic(),
                action=action,
            )
        else:
            await super().close() 

    @database_sync_to_async
    def get_list_seller(self) -> dict | None:
        if self.auth and self.user:
            serializer = StatisticSellerClientSerializer(
                SellerCardEggs.objects.filter(
                        ~Q(balance=0) | ~Q(balance_form_one=0) | ~Q(balance_form_two=0)
                    ).select_related(
                        'requisites', 'documents_contract').prefetch_related(
                        Prefetch('basedealeggsmodel_set',
                    queryset=BaseDealEggsModel.objects.filter(
                        Q(deal_status__gt=1, is_active=True, status=3)))).order_by('balance'), many=True
                )
            return serializer.data    

    @database_sync_to_async
    def get_list_buyer(self) -> dict | None:
        if self.auth and self.user:
            serializer = StatisticBuyerClientSerializer(
                BuyerCardEggs.objects.filter(
                        ~Q(balance=0) | ~Q(balance_form_one=0) | ~Q(balance_form_two=0)
                    ).select_related(
                        'requisites', 'documents_contract').prefetch_related(
                        Prefetch('basedealeggsmodel_set',
                    queryset=BaseDealEggsModel.objects.filter(
                        Q(deal_status__gt=1, is_active=True, status=3)))).order_by('balance'), many=True
                )
            return serializer.data    

    @database_sync_to_async
    def get_list_logic(self) -> dict | None:
        if self.auth and self.user:
            serializer = StatisticLogicClientSerializer(
                LogicCardEggs.objects.filter(
                        ~Q(balance=0) | ~Q(balance_form_one=0) | ~Q(balance_form_two=0)
                    ).select_related(
                        'requisites', 'documents_contract').prefetch_related(
                        Prefetch('basedealeggsmodel_set',
                    queryset=BaseDealEggsModel.objects.filter(
                        Q(deal_status__gt=1, is_active=True, status=3)))).order_by('balance'), many=True
                )
            return serializer.data    

    async def encode_json(self, content):
        return json.dumps(content, ensure_ascii=False)

    async def check_action(self, message: str, action: str, request_id: str):
        allow_methhods = ('delete', 'create', 'update')
        if action in allow_methhods:
            await self.reply(data=message, action=action, request_id=request_id)
