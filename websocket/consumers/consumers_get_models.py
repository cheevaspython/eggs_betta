import json 
import logging
from django.db.models import Q

from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action
from channels.db import database_sync_to_async

from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.applications_serializers import \
    ApplicationBuyerEggsDetailSerializer, ApplicationBuyerEggsWsGetSerializer, \
    ApplicationSellerEggsDetailSerializer, ApplicationSellerEggsWsGetSerializer
from product_eggs.serializers.base_client_serializers import BuyerCardEggsDetailSerializer, \
    LogicCardEggsDetailSerializer, SellerCardEggsDetailSerializer
from product_eggs.serializers.base_deal_serializers import BaseCompDealEggsNameSerializer, \
    BaseDealEggsNameSerializer, CalculateEggsNamesSerializer, \
    ConfirmedCalculateEggsNameSerializer
from product_eggs.services.get_anything.try_to_get_models import get_client_for_inn
from users.serializers import CustomUserSerializer 
from users.models import CustomUser
from websocket.middleware import get_model
from websocket.services.decorator import ws_auth

logger = logging.getLogger(__name__)


class AllModelsSubConsumer(GenericAsyncAPIConsumer):
    queryset = CustomUser.objects.all() 
    serializer_class = CustomUserSerializer
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

    @model_observer(ApplicationFromBuyerBaseEggs)
    @ws_auth
    async def app_buyer_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @app_buyer_activity.serializer
    def app_buyer_activity(self, instance: ApplicationFromBuyerBaseEggs, action, **kwargs):
        if instance.is_active:
            return ApplicationBuyerEggsWsGetSerializer(instance).data
        else:
            return None

    @model_observer(ApplicationFromSellerBaseEggs)
    @ws_auth
    async def app_seller_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @app_seller_activity.serializer
    def app_seller_activity(self, instance: ApplicationFromSellerBaseEggs, action, **kwargs):
        if instance.is_active:
            return ApplicationSellerEggsWsGetSerializer(instance).data
        else:
            return None

    @model_observer(BaseDealEggsModel)
    @ws_auth
    async def calc_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @calc_activity.serializer
    def calc_activity(self, instance: BaseDealEggsModel, action, **kwargs):
        if instance.is_active and instance.status == 1:
            return CalculateEggsNamesSerializer(instance).data
        else:
            return None

    @model_observer(BaseDealEggsModel)
    @ws_auth
    async def conf_calc_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @conf_calc_activity.serializer
    def conf_calc_activity(self, instance: BaseDealEggsModel, action, **kwargs):
        if instance.is_active and instance.status == 2:
            return ConfirmedCalculateEggsNameSerializer(instance).data
        else:
            return None

    @model_observer(BaseDealEggsModel)
    @ws_auth
    async def deal_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @deal_activity.serializer
    def deal_activity(self, instance: BaseDealEggsModel, action, **kwargs):
        if instance.is_active and instance.status == 3:
            return BaseDealEggsNameSerializer(instance).data
        else:
            return None

    @model_observer(BaseDealEggsModel)
    @ws_auth
    async def comp_deal_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @comp_deal_activity.serializer
    def comp_deal_activity(self, instance: BaseDealEggsModel, action, **kwargs):
        if instance.status == 4:
            return BaseCompDealEggsNameSerializer(instance).data
        else:
            return None

    @action()
    @ws_auth
    async def subscribe_to_active_models(self, request_id: str, **kwargs):
        await self.app_buyer_activity.subscribe(request_id=request_id)
        await self.app_seller_activity.subscribe(request_id=request_id)
        await self.calc_activity.subscribe(request_id=request_id)
        await self.conf_calc_activity.subscribe(request_id=request_id)
        await self.deal_activity.subscribe(request_id=request_id)
        await self.comp_deal_activity.subscribe(request_id=request_id)

    @action()
    @ws_auth
    async def get_all_models(self, action: str, **kwargs):
        await self.reply(
            data=await self.get_all_active_models(),
            action=action,
        )

    @action()
    @ws_auth
    async def get_current_model(self, action: str, **kwargs):
        await self.reply(
            data=await self.get_model(kwargs['model']),
            action=action,
        )

    @database_sync_to_async
    def get_all_active_models(self) -> dict | None:
        if self.auth and self.user:
            serializer_app_buyer_eggs = ApplicationBuyerEggsWsGetSerializer(
                ApplicationFromBuyerBaseEggs.objects.filter(
                    is_active=True).select_related(
                        'current_buyer', 'owner', 'current_buyer__requisites'), many=True)
            serializer_app_selller_eggs = ApplicationSellerEggsWsGetSerializer(
                ApplicationFromSellerBaseEggs.objects.filter(
                    is_active=True).select_related(
                        'current_seller', 'owner', 'current_seller__requisites'), many=True)
            serializer_calcs_is_active = CalculateEggsNamesSerializer(
                    BaseDealEggsModel.objects.filter(
                        Q(is_active=True) & Q(status=1)).select_related(
                            'seller', 'buyer', 'owner'), many=True)
            serializer_confirmed_calcs_is_active = ConfirmedCalculateEggsNameSerializer(
                    BaseDealEggsModel.objects.filter(
                        Q(is_active=True) & Q(status=2)).select_related(
                            'seller', 'buyer', 'owner', 'additional_expense', 'current_logic'
                        ), many=True)
            serializer_deal_is_active = BaseDealEggsNameSerializer(
                    BaseDealEggsModel.objects.filter(
                        Q(is_active=True) & Q(status=3)).select_related(
                            'seller', 'buyer', 'owner', 'additional_expense',
                            'current_logic', 'documents',
                        ), many=True)
            serializer_comp_deal_is_active = BaseCompDealEggsNameSerializer(
                    BaseDealEggsModel.objects.filter(
                        Q(is_active=True) & Q(status=4)).select_related(
                            'seller', 'buyer', 'owner', 'additional_expense',
                            'current_logic', 'documents',
                        ), many=True)
            resp_data = {
                'applications_from_buyer_eggs': serializer_app_buyer_eggs.data, 
                'applications_from_seller_eggs': serializer_app_selller_eggs.data,
                'calculates_eggs': serializer_calcs_is_active.data,
                'confirmed_calculates_eggs': serializer_confirmed_calcs_is_active.data,
                'deals_eggs': serializer_deal_is_active.data,
                'comp_deals_eggs': serializer_comp_deal_is_active.data,
                }
            return resp_data

    @database_sync_to_async
    def get_model(self, model: str) -> dict | None:
        if self.auth and self.user:
            match model:
                case 'buyer_app':
                    serializer_app_buyer_eggs = ApplicationBuyerEggsDetailSerializer(
                        ApplicationFromBuyerBaseEggs.objects.filter(
                            is_active=True).select_related(
                                'current_buyer', 'owner', 'current_buyer__requisites'), many=True)
                    return serializer_app_buyer_eggs.data
                case 'seller_app':
                    serializer_app_selller_eggs = ApplicationSellerEggsDetailSerializer(
                        ApplicationFromSellerBaseEggs.objects.filter(
                            is_active=True).select_related(
                                'current_seller', 'owner', 'current_seller__requisites'), many=True)
                    return serializer_app_selller_eggs.data
                case 'calc':
                    serializer_calcs_is_active = CalculateEggsNamesSerializer(
                            BaseDealEggsModel.objects.filter(
                                is_active=True, status=1).select_related(
                                    'seller', 'buyer', 'owner'), many=True)
                    return serializer_calcs_is_active.data
                case 'conf_calc':
                    serializer_confirmed_calcs_is_active = ConfirmedCalculateEggsNameSerializer(
                            BaseDealEggsModel.objects.filter(
                                is_active=True, status=2).select_related(
                                    'seller', 'buyer', 'owner', 'additional_expense', 'current_logic'
                                ), many=True)
                    return serializer_confirmed_calcs_is_active.data
                case 'deal':
                    serializer_deal_is_active = BaseDealEggsNameSerializer(
                            BaseDealEggsModel.objects.filter(
                                is_active=True, status=3).select_related(
                                    'seller', 'buyer', 'owner', 'additional_expense',
                                    'current_logic', 'documents',
                                ), many=True)
                    return serializer_deal_is_active.data
                case 'complete_deal':
                    serializer_comp_deal = BaseCompDealEggsNameSerializer(
                            BaseDealEggsModel.objects.filter(
                                is_active=True, status=4).select_related(
                                    'seller', 'buyer', 'owner', 'additional_expense',
                                    'current_logic', 'documents',
                                ), many=True)
                    return serializer_comp_deal.data
                case _:
                    logging.debug('wrong model name in consumer get model')

    @action()
    @ws_auth
    async def get_client(self, action: str, **kwargs):
        await self.reply(
            data=await self.get_client_detail(kwargs['inn']),
            action=action,
        )

    @database_sync_to_async
    def get_client_detail(self, inn: str) -> dict | None:
        serializers_clients = {
            'BuyerCardEggs': BuyerCardEggsDetailSerializer,
            'SellerCardEggs': SellerCardEggsDetailSerializer,
            'LogicCardEggs': LogicCardEggsDetailSerializer,
        }
        if self.auth and self.user:
            if client := get_client_for_inn(inn):
                return serializers_clients[client.__class__.__name__](client).data

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
