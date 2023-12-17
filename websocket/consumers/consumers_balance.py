import logging

from django.db.models import Prefetch, Q
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.decorators import action
from channels.db import database_sync_to_async

from product_eggs.models.balance import BalanceBaseClientEggs
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.entity import EntityEggs
from product_eggs.serializers.balance_serializers import (
    StatisticBuyerClientSerializer, StatisticLogicClientSerializer,
    StatisticSellerClientSerializer
)
from product_eggs.services.validationerror import custom_error
from users.serializers import CustomUserSerializer
from users.models import CustomUser
from websocket.consumers.consumers import CustomAPIConsumer
from websocket.services.dataclass import ModelsAndSerializers
from websocket.services.decorator import ws_auth

logger = logging.getLogger(__name__)


class BalanceConsumer(CustomAPIConsumer):
    """
    Статистика.
    Подписка на изменения балансов buyer, seller, logic.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    contragents_models: dict[str, ModelsAndSerializers] = {
        'buyer': ModelsAndSerializers(BuyerCardEggs, StatisticBuyerClientSerializer),
        'seller': ModelsAndSerializers(SellerCardEggs, StatisticSellerClientSerializer),
        'logic': ModelsAndSerializers(LogicCardEggs, StatisticLogicClientSerializer),
    }

    @model_observer(BalanceBaseClientEggs)
    @ws_auth
    async def balance_activity(
            self, data: str, action: str, subscribing_request_ids=[], **kwargs):
        for request_id in subscribing_request_ids:
            await self.reply(data=data[0], action=data[1], request_id=request_id)

    @balance_activity.serializer
    def balance_activity_(self, instance: BalanceBaseClientEggs, action, **kwargs):
        contragents_models: dict[str, ModelsAndSerializers] = {
            'buyer': ModelsAndSerializers(BuyerCardEggs, StatisticBuyerClientSerializer),
            'seller': ModelsAndSerializers(SellerCardEggs, StatisticSellerClientSerializer),
            'logic': ModelsAndSerializers(LogicCardEggs, StatisticLogicClientSerializer),
        }
        entity_inn = instance.entity.inn
        if instance.client_buyer:
            action = 'update_buyer'
            cur_model = 'buyer'
            cur_model_inn = instance.client_buyer.pk
        elif instance.client_seller:
            action = 'update_seller'
            cur_model = 'seller'
            cur_model_inn = instance.client_seller.pk
        elif instance.client_logic:
            action = 'update_logic'
            cur_model = 'logic'
            cur_model_inn = instance.client_logic.pk
        else:
            raise custom_error('current balance error in search current client', 433)

        serializer = contragents_models[cur_model].serializer(
            contragents_models[cur_model].model.objects.filter(
                Q(cur_balance__entity__inn=entity_inn), inn=cur_model_inn
        ).select_related(
            'requisites', 'manager', 'guest', 'documents_contract'
        ).prefetch_related(
            Prefetch('cur_balance', queryset=BalanceBaseClientEggs.objects.filter(
                entity__inn=entity_inn
        ))).prefetch_related(
        Prefetch(
            'basedealeggsmodel_set', queryset=BaseDealEggsModel.objects.filter(
                Q(deal_status__gte=3, is_active=True, status__gt=1, entity__inn=entity_inn)))
        ).order_by('cur_balance__balance'), many=True)

        result = {
            'current_entity': entity_inn,
            'serializer_data': serializer.data
        }
        return [result, action]

    @action()
    @ws_auth
    async def subscribe_to_balance(self, request_id: str, **kwargs):
        await self.balance_activity.subscribe(request_id=request_id)

    @action()
    @ws_auth
    async def get_balance(self,
            action: str,
            cur_model: str,
            cur_model_inn: str | None = None,
            entity_inn: str | None = None, **kwargs
        ):
        if cur_model_inn and entity_inn:
            await self.reply(
                data=await self.get_current_client(cur_model, cur_model_inn, entity_inn),
                action=action + '_' + cur_model + '_param',
            )
        else:
            await self.reply(
                data=await self.get_clients_balance(cur_model),
                action=action + '_' + cur_model,
            )

    @database_sync_to_async
    def get_clients_balance(self, cur_model: str) -> dict:
        return_book = dict()
        entitys = EntityEggs.objects.all()
        if cur_model in self.contragents_models.keys():
            for cur_entity in entitys:
                serializer = self.contragents_models[cur_model].serializer(
                    self.contragents_models[cur_model].model.objects.filter(
                    Q(cur_balance__entity__inn=cur_entity.inn) & ~Q(cur_balance__balance=0) & ~Q(cur_balance=None)
                ).select_related(
                    'requisites', 'manager', 'guest', 'documents_contract'
                ).prefetch_related(
                    Prefetch('cur_balance', queryset=BalanceBaseClientEggs.objects.filter(
                        entity__inn=cur_entity.inn
                ))).prefetch_related(
                    Prefetch(
                        'basedealeggsmodel_set', queryset=BaseDealEggsModel.objects.filter(
                            Q(deal_status__gte=3, is_active=True, status__gt=1, entity__inn=cur_entity.inn)))
                ).order_by('cur_balance__balance'), many=True)
                if serializer.data:
                    return_book.update({cur_entity.inn: serializer.data})
        return return_book

    @database_sync_to_async
    def get_current_client(
            self,
            cur_model: str,
            cur_model_inn: str,
            entity_inn: str
        ) -> dict:

        return_book = dict()

        if cur_model in self.contragents_models.keys():
            serializer = self.contragents_models[cur_model].serializer(
                self.contragents_models[cur_model].model.objects.filter(
                    Q(cur_balance__entity__inn=entity_inn), inn=cur_model_inn
            ).select_related(
                'requisites', 'manager', 'guest', 'documents_contract'
            ).prefetch_related(
                Prefetch('cur_balance', queryset=BalanceBaseClientEggs.objects.filter(
                    entity__inn=entity_inn
            ))).prefetch_related(
            Prefetch(
                'basedealeggsmodel_set', queryset=BaseDealEggsModel.objects.filter(
                    Q(deal_status__gte=3, is_active=True, status__gt=1, entity__inn=entity_inn)))
            ).order_by('cur_balance__balance'), many=True)
            if serializer.data:
                return_book.update({entity_inn: serializer.data})

        return return_book








