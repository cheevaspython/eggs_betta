import json
import logging

from django.contrib.auth import get_user_model
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action
from channels.db import database_sync_to_async

from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.serializers.applications_serializers import ApplicationBuyerEggsSerializer, \
    ApplicationBuyerEggsSerializerSideBar, ApplicationSellerEggsSerializer, \
    ApplicationSellerEggsSerializerSideBar
from product_eggs.services.raw.left_side_bar import app_buyer_is_active_owner, \
    app_seller_is_active_owner, calc_is_active_where_doc_id_as_deal_id, \
    conf_calc_is_active_where_doc_id_as_deal_id, deal_is_active_where_doc_id_as_deal_id
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.base_deal_serializers import BaseDealEggsSerializer, \
    CalculateEggsSerializer, CalculateEggsSerializerSideBar, ConfirmedCalculateEggsSerializer, \
    ConfirmedCalculateEggsSerializerSideBar, DealEggsSerializerSideBar
from users.serializers import CustomUserSerializer 
from users.models import CustomUser
from websocket.middleware import get_model

User = get_user_model()
logger = logging.getLogger(__name__)


class SideBarSubConsumer(GenericAsyncAPIConsumer):
    queryset = CustomUser.objects.all() 
    serializer_class = CustomUserSerializer
    auth = False
    user = None

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
    async def subscribe_to_side_bar_eggs(self, request_id: str, **kwargs):
        if self.auth:
            await self.seller_app_activity.subscribe(
                request_id=request_id, user=self.user)
            await self.buyer_app_activity.subscribe(
                request_id=request_id, user=self.user)
            await self.calc_activity.subscribe(
                request_id=request_id, user=self.user)
            await self.conf_calc_activity.subscribe(
                request_id=request_id, user=self.user)
            await self.base_deal_activity.subscribe(
                request_id=request_id, user=self.user)
        else:
            await super().close() 

    @model_observer(ApplicationFromSellerBaseEggs, serializer_class=ApplicationSellerEggsSerializer)
    async def seller_app_activity(
            self, seller_app: str, action: str, subscribing_request_ids=[], **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.check_action(message=seller_app, action=action, request_id=request_id)
        else:
            await super().close() 

    @model_observer(ApplicationFromBuyerBaseEggs, serializer_class=ApplicationBuyerEggsSerializer)
    async def buyer_app_activity(
            self, buyer_app: str, action: str, subscribing_request_ids=[], **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.check_action(message=buyer_app, action=action, request_id=request_id)
        else:
            await super().close() 

    @model_observer(BaseDealEggsModel, serializer_class=CalculateEggsSerializer)
    async def calc_activity(
            self, base_deal: str, action: str, subscribing_request_ids=[], **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.check_action(message=base_deal, action=action, request_id=request_id)
        else:
            await super().close() 

    @model_observer(BaseDealEggsModel, serializer_class=ConfirmedCalculateEggsSerializer)
    async def conf_calc_activity(
            self, base_deal: str, action: str, subscribing_request_ids=[], **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.check_action(message=base_deal, action=action, request_id=request_id)
        else:
            await super().close() 

    @model_observer(BaseDealEggsModel, serializer_class=BaseDealEggsSerializer)
    async def base_deal_activity(
            self, base_deal: str, action: str, subscribing_request_ids=[], **kwargs):
        if self.auth:
            for request_id in subscribing_request_ids:
                await self.check_action(message=base_deal, action=action, request_id=request_id)
        else:
            await super().close() 

    @seller_app_activity.groups_for_signal
    def seller_app_activity(self, instance: ApplicationFromSellerBaseEggs, **kwargs):
        if instance.is_active:
            yield f'-owner__{instance.owner_id}' 

    @buyer_app_activity.groups_for_signal
    def buyer_app_activity(self, instance: ApplicationFromBuyerBaseEggs, **kwargs):
        if instance.is_active:
            yield f'-owner__{instance.owner_id}'

    @calc_activity.groups_for_signal
    def calc_activity(self, instance: BaseDealEggsModel, **kwargs):
        if instance.is_active and instance.status == 1:
            yield f'-owner__{instance.owner_id}'

    @conf_calc_activity.groups_for_signal
    def conf_calc_activity(self, instance: BaseDealEggsModel, **kwargs):
        if instance.is_active and instance.status == 2:
            yield f'-owner__{instance.owner_id}'

    @base_deal_activity.groups_for_signal
    def base_deal_activity(self, instance: BaseDealEggsModel, **kwargs):
        if instance.is_active and instance.status == 3:
            yield f'-owner__{instance.owner_id}'

    @seller_app_activity.groups_for_consumer
    def seller_app_activity(self, school=None, classroom=None, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'  

    @buyer_app_activity.groups_for_consumer
    def buyer_app_activity(self, school=None, classroom=None, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'

    @calc_activity.groups_for_consumer
    def calc_activity(self, school=None, classroom=None, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'

    @conf_calc_activity.groups_for_consumer
    def conf_calc_activity(self, school=None, classroom=None, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'

    @base_deal_activity.groups_for_consumer
    def base_deal_activity(self, school=None, classroom=None, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'

    @database_sync_to_async
    def get_current_side_bar(self) -> dict | None:
        if self.auth and self.user:
            serializer_current_user_app_buyer_eggs = ApplicationBuyerEggsSerializerSideBar(
                app_buyer_is_active_owner(self.user.pk), many=True)
            serializer_current_user_app_selller_eggs = ApplicationSellerEggsSerializerSideBar(
                app_seller_is_active_owner(self.user.pk), many=True)
            calcs_user_is_active = CalculateEggsSerializerSideBar(
                calc_is_active_where_doc_id_as_deal_id(self.user.pk), many=True)
            confirmed_calcs_user_is_active = ConfirmedCalculateEggsSerializerSideBar(
                conf_calc_is_active_where_doc_id_as_deal_id(self.user.pk), many=True)
            deal_side_bar = DealEggsSerializerSideBar(
                deal_is_active_where_doc_id_as_deal_id(self.user.pk), many=True)
            resp_data = {
                'current_user_application_from_buyer_eggs': serializer_current_user_app_buyer_eggs.data, 
                'current_user_application_from_seller_eggs': serializer_current_user_app_selller_eggs.data,
                'current_user_calculate_eggs': calcs_user_is_active.data,
                'current_user_confirmed_calculate_eggs': confirmed_calcs_user_is_active.data,
                'current_user_deal_eggs': deal_side_bar.data,
                }
            return resp_data

    @action()
    async def get_side_bar(self, action: str, **kwargs):
        if self.auth:
            await self.reply(
                data=await self.get_current_side_bar(),
                action=action,
            )
        else:
            await super().close() 

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
