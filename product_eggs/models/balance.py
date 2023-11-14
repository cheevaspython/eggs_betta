from django.db import models
from django.db.models.signals import post_delete
from rest_framework import serializers

from general_layout.balance.models.balance import BalanceBaseClient

from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.entity import EntityEggs
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.receivers import (
    change_client_entity_recever_delete
)
from product_eggs.services.tails_calc import calc_client_tail_debt
from product_eggs.tasks.entity_client import change_client_entity_list


class BalanceBaseClientEggs(BalanceBaseClient):

    class Meta:
        db_table = 'BalanceBaseClientEggs'
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ['pk']

    entity = models.ForeignKey(
        EntityEggs, related_name='entity',
        verbose_name='Юр. лицо',
        on_delete=models.PROTECT,
    )
    tails = models.OneToOneField(
        TailsContragentModelEggs,
        on_delete=models.PROTECT,
        null=True, blank=True,
        default=None,
        related_name='cur_balance',
        verbose_name='Депозит',
    )
    client_buyer = models.ForeignKey(
        BuyerCardEggs,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='cur_balance',
        verbose_name='Покупатель',
    )
    client_seller = models.ForeignKey(
        SellerCardEggs,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='cur_balance',
        verbose_name='Продавец',
    )
    client_logic = models.ForeignKey(
        LogicCardEggs,
        on_delete=models.PROTECT,
        null=True, blank=True,
        related_name='cur_balance',
        verbose_name='Перевозчик',
    )
    # pay_type = models.PositiveSmallIntegerField(
    #     verbose_name='Тип оплаты', choices=PAY_TYPE,
    #     default=1,
    # )

    def check_lock_relations(self):
        if self.client_seller != self.__client_seller:
            raise serializers.ValidationError(
                f'Balance model №{self.pk} wrong'
            )
        if self.client_buyer != self.__client_buyer:
            raise serializers.ValidationError(
                f'Balance model №{self.pk} wrong'
            )
        if self.client_logic != self.__client_logic:
            raise serializers.ValidationError(
                f'Balance model №{self.pk} wrong'
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__client_seller = self.client_seller
        self.__client_buyer = self.client_buyer
        self.__client_logic = self.client_logic

    def save(self, *args, **kwargs):
        creating = not bool(self.pk)
        if creating:
            res =  super().save(*args, **kwargs)
            change_client_entity_list(self)
            return res

        self.check_lock_relations()
        if self.tails:
            self.balance = (
                self.balance_form_one +
                self.balance_form_two +
                calc_client_tail_debt(self.tails)
            )
        else:
            self.balance = (
                self.balance_form_one +
                self.balance_form_two
            )
        return super().save(*args, **kwargs)

    def __str__(self):
        if self.client_buyer:
            return f'Баланс {self.pk}, Юр. лицо {self.entity.name}, покупатель {self.client_buyer}.'
        elif self.client_seller:
            return f'Баланс {self.pk}, Юр. лицо {self.entity.name}, продавец {self.client_seller}.'
        elif self.client_logic:
            return f'Баланс {self.pk}, Юр. лицо {self.entity.name}, перевозчик {self.client_logic}.'
        else:
            return f'Баланс {self.pk}, Юр. лицо {self.entity.name}.'


post_delete.connect(change_client_entity_recever_delete, sender=BalanceBaseClientEggs, dispatch_uid="test_uid")
