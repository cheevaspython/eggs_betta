import logging

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action

from channels.db import database_sync_to_async
from rest_framework import serializers

from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.applications import (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
)
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.comment import CommentEggs
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.serializers.applications_serializers import (
    ApplicationBuyerEggsWsGetSerializer,
    ApplicationSellerEggsWsGetSerializer
)
from product_eggs.serializers.base_client_serializers import (
    BuyerCardEggsDetailSerializer, LogicCardEggsDetailSerializer,
    SellerCardEggsDetailSerializer
)
from product_eggs.serializers.base_deal_serializers import (
    BaseCompDealEggsNameSerializerObserver,
    BaseDealEggsNameSerializerObserver,
    CalculateEggsNamesSerializerObserver,
    ConfirmedCalculateEggsNameSerializerObserver
)
from product_eggs.services.base_deal.db_orm import (
    get_base_deal_orm_request, get_base_deal_orm_request_param
)
from product_eggs.services.get_anything.try_to_get_models import get_client_for_inn

from users.serializers import CustomUserSerializer
from users.models import CustomUser

from websocket.consumers.consumers import CustomAPIConsumer
from websocket.services.decorator import ws_auth

logger = logging.getLogger(__name__)


class AllModelsSubConsumer(CustomAPIConsumer):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    @model_observer(ApplicationFromBuyerBaseEggs, serializer_class=ApplicationBuyerEggsWsGetSerializer)
    @ws_auth
    async def app_buyer_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @model_observer(CommentEggs)
    @ws_auth
    async def comment_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @comment_activity.serializer
    def comment_activity(self, instance: CommentEggs, action, **kwargs):
        try:
            base_deal = BaseDealEggsModel.objects.get(comment_json=instance.pk)
            match base_deal.status:
                case 1:
                    return CalculateEggsNamesSerializerObserver(base_deal).data
                case 2:
                    return ConfirmedCalculateEggsNameSerializerObserver(base_deal).data
                case 3:
                    return BaseDealEggsNameSerializerObserver(base_deal).data
                case 4:
                    return BaseCompDealEggsNameSerializerObserver(base_deal).data #TODO TEST
        except ObjectDoesNotExist:
            pass
        try:
            buyer_app = ApplicationFromBuyerBaseEggs.objects.get(comment_json=instance.pk)
            return ApplicationBuyerEggsWsGetSerializer(buyer_app).data
        except ObjectDoesNotExist:
            pass
        try:
            seller_app = ApplicationFromSellerBaseEggs.objects.get(comment_json=instance.pk)
            return ApplicationSellerEggsWsGetSerializer(seller_app).data
        except ObjectDoesNotExist:
            pass

    @model_observer(AdditionalExpenseEggs)
    @ws_auth
    async def additional_expense_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @additional_expense_activity.serializer
    def additional_expense_activity(self, instance: AdditionalExpenseEggs, action, **kwargs):
        try:
            base_deal = BaseDealEggsModel.objects.get(additional_expense_id=instance.pk)
            if base_deal.status == 2:
                return ConfirmedCalculateEggsNameSerializerObserver(base_deal).data
            elif base_deal.status == 3:
                return BaseDealEggsNameSerializerObserver(base_deal).data
        except ObjectDoesNotExist as e:
            logging.debug('ws: docs activity', e)

    @model_observer(ApplicationFromSellerBaseEggs, serializer_class=ApplicationSellerEggsWsGetSerializer)
    @ws_auth
    async def app_seller_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @model_observer(DocumentsDealEggsModel)
    @ws_auth
    async def deal_docs_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @deal_docs_activity.serializer
    def deal_docs_activity(self, instance: DocumentsDealEggsModel, action, **kwargs):
        try:
            deal = BaseDealEggsModel.objects.get(documents_id=instance.pk)
            return BaseDealEggsNameSerializerObserver(deal).data
        except ObjectDoesNotExist as e:
            logging.debug('ws: docs activity', e)

    @model_observer(BaseDealEggsModel)
    @ws_auth
    async def base_deal_activity(self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            if data:
                await self.reply(data=data, action=action, request_id=request_id)

    @base_deal_activity.serializer
    def base_deal_activity(self, instance: BaseDealEggsModel, action, **kwargs):
        match instance.status:
            case 1:
                return CalculateEggsNamesSerializerObserver(instance).data
            case 2:
                return ConfirmedCalculateEggsNameSerializerObserver(instance).data
            case 3:
                return BaseDealEggsNameSerializerObserver(instance).data
            case 4:
                return BaseCompDealEggsNameSerializerObserver(instance).data
            case _:
                return None

    @action()
    @ws_auth
    async def subscribe_to_active_models(self, request_id: str, **kwargs):
        await self.app_buyer_activity.subscribe(request_id=request_id)
        await self.app_seller_activity.subscribe(request_id=request_id)
        await self.base_deal_activity.subscribe(request_id=request_id)
        await self.deal_docs_activity.subscribe(request_id=request_id)
        await self.additional_expense_activity.subscribe(request_id=request_id)
        await self.comment_activity.subscribe(request_id=request_id)

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
            data=await self.get_cur_model(kwargs['model'], kwargs['model_pk']),
            action=action,
        )

    @database_sync_to_async
    def get_all_active_models(self) -> dict | None:
        if self.auth and self.user:
            serializer_app_buyer_eggs = ApplicationBuyerEggsWsGetSerializer(
                ApplicationFromBuyerBaseEggs.objects.filter(
                    Q(is_active=True) & Q(is_actual=True)).select_related(
                        'current_buyer', 'owner', 'comment_json', 'current_buyer__requisites'
                    ), many=True)
            serializer_app_selller_eggs = ApplicationSellerEggsWsGetSerializer(
                ApplicationFromSellerBaseEggs.objects.filter(
                    Q(is_active=True) & Q(is_actual=True)).select_related(
                        'current_seller', 'owner', 'comment_json', 'current_seller__requisites'
                    ), many=True)
            serializer_calcs_is_active = get_base_deal_orm_request(1)
            serializer_confirmed_calcs_is_active = get_base_deal_orm_request(2)
            serializer_deal_is_active = get_base_deal_orm_request(3)
            serializer_comp_deal_is_active = get_base_deal_orm_request(4)
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
    def get_cur_model(self, model: str, model_pk: int) -> dict:
        if self.auth and self.user:
            match model:
                case 'buyer_app':
                    serializer_app_buyer_eggs = ApplicationBuyerEggsWsGetSerializer(
                        ApplicationFromBuyerBaseEggs.objects.filter(
                            pk=model_pk).select_related(
                                'current_buyer', 'owner', 'comment_json', 'current_buyer__requisites'
                            ), many=True)
                    return serializer_app_buyer_eggs.data
                case 'seller_app':
                    serializer_app_selller_eggs = ApplicationSellerEggsWsGetSerializer(
                        ApplicationFromSellerBaseEggs.objects.filter(
                            pk=model_pk).select_related(
                                'current_seller', 'owner', 'comment_json', 'current_seller__requisites'
                            ), many=True)
                    return serializer_app_selller_eggs.data
                case 'calc':
                    serializer_calcs_is_active = get_base_deal_orm_request_param(1, model_pk)
                    return serializer_calcs_is_active.data
                case 'conf_calc':
                    serializer_confirmed_calcs_is_active = get_base_deal_orm_request_param(2, model_pk)
                    return serializer_confirmed_calcs_is_active.data
                case 'deal':
                    serializer_deal_is_active = get_base_deal_orm_request_param(3, model_pk)
                    return serializer_deal_is_active.data
                case 'complete_deal':
                    serializer_comp_deal = get_base_deal_orm_request_param(4, model_pk)
                    return serializer_comp_deal.data
                case _:
                    raise serializers.ValidationError('wrong model name in ws consumer get model')
        raise serializers.ValidationError('ws get_models error in auth or request user')

    @action()
    @ws_auth
    async def get_client(self, action: str, **kwargs):
        await self.reply(
            data=await self.get_client_detail(kwargs['client_inn'], kwargs['client_type']),
            action=action,
        )

    @database_sync_to_async
    def get_client_detail(self, client_inn: str, client_type: str) -> dict | None:
        serializers_clients = {
            'BuyerCardEggs': BuyerCardEggsDetailSerializer,
            'SellerCardEggs': SellerCardEggsDetailSerializer,
            'LogicCardEggs': LogicCardEggsDetailSerializer,
        }
        if self.auth and self.user:
            if client := get_client_for_inn(client_inn, client_type):
                return serializers_clients[client.__class__.__name__](client).data











