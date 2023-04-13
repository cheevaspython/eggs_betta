from django.db import models 

from general_layout.bases.models import AbstractClientCard, \
    AbstractAddressCard, LogicCard, AbstractWarehouseCard
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.models.documents import DocumentsContractEggsModel, \
    DocumentsBuyerEggsModel
from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.services.decorators import try_decorator_param
from users.models import CustomUser


@try_decorator_param(('KeyError',), return_value=0)
def calc_client_tail_debt(tail: TailsContragentModelEggs):
    return tail.current_tail_form_one + tail.current_tail_form_two


class BuyerCardEggs(AbstractClientCard, AbstractWarehouseCard):

    class Meta:
        db_table = 'BuyerCardEggs'
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['pk']
        
    docs_cash = models.OneToOneField(
        DocumentsBuyerEggsModel, on_delete=models.PROTECT, 
        verbose_name='Покупатель доки наличка', null=True,
    )
    tails = models.OneToOneField(
        TailsContragentModelEggs, on_delete=models.PROTECT, 
        verbose_name='Депозит', null=True,
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
    manager_details = models.CharField(
        max_length=100,
        verbose_name='Менеджер детали', null=True, 
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
        self.balance = (self.balance_form_one + 
            self.balance_form_two + calc_client_tail_debt(self.tails))

        return super().save(*args, **kwargs)

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
        verbose_name='Депозит', null=True,
    )
    manager = models.ForeignKey(
        CustomUser, related_name='seller_manager',
        verbose_name='Менеджер', 
        on_delete=models.SET_NULL, null=True,
    )
    manager_details = models.CharField(
        max_length=100, verbose_name='Менеджер детали',
        null=True, blank=True,
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

    def save(self, *args, **kwargs):
        self.balance = (self.balance_form_one + 
            self.balance_form_two + calc_client_tail_debt(self.tails))

        return super().save(*args, **kwargs)

    def __str__(self):
        return f'Продавец {self.name}'


class LogicCardEggs(LogicCard):

    class Meta:
        db_table = 'LogicEggs'
        verbose_name = 'Логист'
        verbose_name_plural = 'Логист'
        ordering = ['pk']

    requisites = models.OneToOneField(
        RequisitesEggs, on_delete=models.PROTECT, 
        verbose_name='Реквизиты', null=True, blank=True,
    )
    documents_contract = models.OneToOneField(
        DocumentsContractEggsModel, on_delete=models.PROTECT, 
        verbose_name='Документы (Договора)', null=True,
    )
    def __str__(self):
        return f'Логист {self.name}'
