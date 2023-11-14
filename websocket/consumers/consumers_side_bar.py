import logging

from django.db.models import F, Q

from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action

from channels.db import database_sync_to_async

from product_eggs.models.applications import (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
)
from product_eggs.serializers.applications_serializers import (
    ApplicationBuyerEggsSerializerSideBar,
    ApplicationBuyerEggsSerializerSideBarObserver,
    ApplicationSellerEggsSerializerSideBar,
    ApplicationSellerEggsSerializerSideBarObserver
)
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.base_deal_serializers import (
    CalculateEggsSerializerSideBar,
    CalculateEggsSerializerSideBarObserver,
    ConfirmedCalculateEggsSerializerSideBar,
    ConfirmedCalculateEggsSerializerSideBarObserver,
    DealEggsSerializerSideBar,
    DealEggsSerializerSideBarObserver
)
from users.serializers import CustomUserSerializer
from users.models import CustomUser

from websocket.consumers.consumers import CustomAPIConsumer
from websocket.services.decorator import ws_auth

logger = logging.getLogger(__name__)


class SideBarSubConsumer(CustomAPIConsumer):
    """ws for sidebar"""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

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

    @model_observer(ApplicationFromSellerBaseEggs, serializer_class=ApplicationSellerEggsSerializerSideBarObserver)
    @ws_auth
    async def seller_app_activity(
            self, seller_app: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            await self.check_action(message=seller_app, action=action, request_id=request_id)

    @model_observer(ApplicationFromBuyerBaseEggs, serializer_class=ApplicationBuyerEggsSerializerSideBarObserver)
    @ws_auth
    async def buyer_app_activity(
            self, buyer_app: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            await self.check_action(message=buyer_app, action=action, request_id=request_id)

    @model_observer(BaseDealEggsModel, serializer_class=CalculateEggsSerializerSideBarObserver)
    @ws_auth
    async def calc_activity(
            self, base_deal: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            await self.check_action_side_bar(message=base_deal, action=action, request_id=request_id)

    @model_observer(BaseDealEggsModel, serializer_class=ConfirmedCalculateEggsSerializerSideBarObserver)
    @ws_auth
    async def conf_calc_activity(
            self, base_deal: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            await self.check_action_side_bar(message=base_deal, action=action, request_id=request_id)

    @model_observer(BaseDealEggsModel, serializer_class=DealEggsSerializerSideBarObserver)
    @ws_auth
    async def base_deal_activity(
            self, base_deal: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            await self.check_action(message=base_deal, action=action, request_id=request_id)

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
    def seller_app_activity(self, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'

    @buyer_app_activity.groups_for_consumer
    def buyer_app_activity(self, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'

    @calc_activity.groups_for_consumer
    def calc_activity(self, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'

    @conf_calc_activity.groups_for_consumer
    def conf_calc_activity(self, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'

    @base_deal_activity.groups_for_consumer
    def base_deal_activity(self, **kwargs):
        if isinstance(kwargs['user'], CustomUser):
            yield f'-owner__{kwargs["user"].pk}'

    @database_sync_to_async
    def get_current_side_bar(self) -> dict | None:
        if self.auth and self.user:    
            serializer_current_user_app_buyer_eggs = ApplicationBuyerEggsSerializerSideBar(
                ApplicationFromBuyerBaseEggs.objects.select_related(
                    'current_buyer'
                ).filter(Q(is_active=True) & Q(owner_id=self.user.pk)).annotate(
                    name=F('current_buyer__requisites__name')
            ).values('id', 'is_actual', 'await_add_cost', 'name'), many=True)

            serializer_current_user_app_selller_eggs = ApplicationSellerEggsSerializerSideBar(
                ApplicationFromSellerBaseEggs.objects.select_related(
                    'current_seller'
                ).filter(Q(is_active=True) & Q(owner_id=self.user.pk)).annotate(
                    name=F('current_seller__requisites__name')
            ).values('id', 'is_actual', 'await_add_cost', 'name'), many=True)

            calcs_user_is_active = CalculateEggsSerializerSideBar(
                BaseDealEggsModel.objects.select_related(
                    'buyer', 'seller', 'owner'
                ).filter(Q(status=1) & Q(is_active=True) & Q(owner_id=self.user.pk)).annotate(
                    seller_name_orm=F('seller__requisites__name'),
                    buyer_name_orm=F('buyer__requisites__name')
                ).values(
                    'id', 'documents_id', 'deal_our_pay_amount',
                    'deal_buyer_pay_amount', 'logic_our_pay_amount',
                    'is_active', 'status', 'owner_id', 'seller_name_orm', 'buyer_name_orm',
                ), many=True)

            confirmed_calcs_user_is_active = ConfirmedCalculateEggsSerializerSideBar(
                BaseDealEggsModel.objects.select_related(
                    'buyer', 'seller', 'owner'
                ).filter(Q(status=2) & Q(is_active=True) & Q(owner_id=self.user.pk)).annotate(
                    seller_name_orm=F('seller__requisites__name'),
                    buyer_name_orm=F('buyer__requisites__name')
                ).values(
                    'id', 'documents_id', 'deal_our_pay_amount',
                    'deal_buyer_pay_amount', 'logic_our_pay_amount',
                    'is_active', 'status', 'owner_id', 'seller_name_orm', 'buyer_name_orm',
                ), many=True)

            deal_side_bar = DealEggsSerializerSideBar(
                BaseDealEggsModel.objects.select_related(
                    'buyer', 'seller', 'owner'
                ).filter(Q(status=3) & Q(is_active=True) & Q(owner_id=self.user.pk)).annotate(
                    seller_name_orm=F('seller__requisites__name'),
                    buyer_name_orm=F('buyer__requisites__name')
                ).values(
                    'id', 'documents_id', 'deal_our_pay_amount',
                    'deal_buyer_pay_amount', 'logic_our_pay_amount', 'deal_status',
                    'is_active', 'status', 'owner_id', 'seller_name_orm', 'buyer_name_orm',
                ), many=True)

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

