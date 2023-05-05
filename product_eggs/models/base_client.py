from django.db import models 

from general_layout.bases.models import AbstractClientCard, \
    AbstractAddressCard, LogicCard, AbstractWarehouseCard
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.models.documents import DocumentsContractEggsModel
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.tails_calc import calc_client_tail_debt
from users.models import CustomUser


class BuyerCardEggs(AbstractClientCard, AbstractWarehouseCard):

    class Meta:
        db_table = 'BuyerCardEggs'
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['pk']
        
    tails = models.OneToOneField(
        TailsContragentModelEggs, on_delete=models.PROTECT, 
        null=True, blank=True, 
        verbose_name='Депозит',
    )
    requisites = models.OneToOneField(
        RequisitesEggs, on_delete=models.PROTECT, 
        verbose_name='Реквизиты', null=True,
    )
    pay_limit = models.BigIntegerField(
        null=True, blank=True, default=0,
        verbose_name='Лимит задолженности',
    )
    pay_limit_cash = models.BigIntegerField(
        null=True, blank=True, default=0,
        verbose_name='Лимит задолженности, нал',
    )
    manager = models.ForeignKey(
        CustomUser, related_name='buyer_manager',
        verbose_name='Менеджер',
        on_delete=models.SET_NULL, null=True
    )
    guest = models.ForeignKey(
        CustomUser, related_name='guest_manager_buyer',
        verbose_name='Гость-Менеджер',
        on_delete=models.SET_NULL, null=True
    )
    balance = models.FloatField(
        default=0, null=True,
        verbose_name='Баланс',
    )
    balance_form_one = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Баланс по форме 1', 
    )
    balance_form_two = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Баланс по форме 2', 
    )
    documents_contract = models.OneToOneField(
        DocumentsContractEggsModel, 
        on_delete=models.PROTECT, 
        verbose_name='Документы (Договора)', null=True
    )
    def save(self, *args, **kwargs):
        if self.tails:
            self.balance = (self.balance_form_one + 
                self.balance_form_two + calc_client_tail_debt(self.tails))
        else:
            self.balance = (self.balance_form_one + 
                self.balance_form_two)

        return super(BuyerCardEggs, self).save(*args, **kwargs)

    def __str__(self):
        return f'Покупатель {self.name}'
    

class SellerCardEggs(AbstractClientCard, AbstractAddressCard):
    
    class Meta:
        db_table = 'SellerCardEggs'
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
        ordering = ['pk']

    requisites = models.OneToOneField(
        RequisitesEggs, on_delete=models.PROTECT, 
        verbose_name='Реквизиты', null=True,
    )
    documents_contract = models.OneToOneField(
        DocumentsContractEggsModel, on_delete=models.PROTECT, 
        verbose_name='Документы (Договора)', null=True,
    )
    tails = models.OneToOneField(
        TailsContragentModelEggs, on_delete=models.PROTECT, 
        null=True, blank=True, 
        verbose_name='Депозит', 
    )
    manager = models.ForeignKey(
        CustomUser, related_name='seller_manager',
        verbose_name='Менеджер', 
        on_delete=models.SET_NULL, null=True,
    )
    balance = models.FloatField(
        default=0, null=True,
        verbose_name='Баланс',
    )
    balance_form_one = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Баланс по форме 1', 
    )
    balance_form_two = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Баланс по форме 2', 
    )
    guest = models.ForeignKey(
        CustomUser, related_name='guest_manager_seller',
        verbose_name='Гость-Менеджер',
        on_delete=models.SET_NULL, null=True
    )

    def save(self, *args, **kwargs):
        if self.tails:
            self.balance = (self.balance_form_one + 
                self.balance_form_two + calc_client_tail_debt(self.tails))
        else:
            self.balance = (self.balance_form_one + 
                self.balance_form_two)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Продавец {self.name}'


class LogicCardEggs(LogicCard):

    class Meta:
        db_table = 'LogicCardEggs'
        verbose_name = 'Перевозчик'
        verbose_name_plural = 'Перевозчики'
        ordering = ['pk']

    requisites = models.OneToOneField(
        RequisitesEggs, on_delete=models.PROTECT, 
        verbose_name='Реквизиты', null=True, blank=True,
    )
    balance = models.FloatField(
        default=0, null=True,
        verbose_name='Баланс',
    )
    balance_form_one = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Баланс по форме 1', 
    )
    balance_form_two = models.FloatField(
        null=True, blank=True, default=0,
        verbose_name='Баланс по форме 2', 
    )
    documents_contract = models.OneToOneField(
        DocumentsContractEggsModel, on_delete=models.PROTECT, 
        verbose_name='Документы (Договора)', null=True,
    )
    guest = models.ForeignKey(
        CustomUser, related_name='guest_manager_logic',
        verbose_name='Гость-Менеджер',
        on_delete=models.SET_NULL, null=True
    )
    tails = models.OneToOneField(
        TailsContragentModelEggs, on_delete=models.PROTECT, 
        null=True, blank=True, 
        verbose_name='Депозит',
    )
    def save(self, *args, **kwargs):
        self.balance = (self.balance_form_one + 
            self.balance_form_two)

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Перевозчик {self.name}'
