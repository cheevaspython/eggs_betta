from django.db import models

from general_layout.bases.models import (
    AbstractClientCard, AbstractAddressCard,
    LogicCard, AbstractWarehouseCard
)
from product_eggs.models.contact_person import ContactPersonEggs
from product_eggs.models.entity import EntityEggs
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.models.documents import DocumentsContractEggsModel
from product_eggs.services.validation.validate_fields import validate_guest_role
from users.models import CustomUser


class BuyerCardEggs(AbstractClientCard, AbstractWarehouseCard):

    class Meta:
        db_table = 'BuyerCardEggs'
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
        ordering = ['inn']

    region = models.CharField(
        max_length=100, verbose_name='Регион',
    )
    contact_person = models.ManyToManyField(
        ContactPersonEggs, related_name="contact_person_buyer",
        blank=True,
    )
    requisites = models.ForeignKey(
        RequisitesEggs, on_delete=models.PROTECT,
        verbose_name='Реквизиты', null=True,
    )
    manager = models.ForeignKey(
        CustomUser, related_name='buyer_manager',
        verbose_name='Менеджер',
        on_delete=models.SET_NULL, null=True
    )
    guest = models.ForeignKey(
        CustomUser, related_name='guest_manager_buyer',
        verbose_name='Гость-Менеджер',
        on_delete=models.SET_NULL, null=True, blank=True,
        validators=[validate_guest_role],
    )
    documents_contract = models.OneToOneField(
        DocumentsContractEggsModel,
        on_delete=models.PROTECT,
        verbose_name='Документы (Договора)', null=True
    )
    entitys = models.ManyToManyField(
        EntityEggs,
        related_name="client_buyer",
        blank=True,
    )

    def __str__(self):
        if self.requisites:
            return f'Покупатель {self.requisites.name}'
        else:
            return f'Покупатель/{self.inn}'


class SellerCardEggs(AbstractClientCard, AbstractAddressCard):

    class Meta:
        db_table = 'SellerCardEggs'
        verbose_name = 'Продавец'
        verbose_name_plural = 'Продавцы'
        ordering = ['inn']

    region = models.CharField(
        max_length=100, verbose_name='Регион',
    )
    requisites = models.ForeignKey(
        RequisitesEggs, on_delete=models.PROTECT,
        verbose_name='Реквизиты', null=True,
    )
    documents_contract = models.OneToOneField(
        DocumentsContractEggsModel, on_delete=models.PROTECT,
        verbose_name='Документы (Договора)', null=True,
    )
    contact_person = models.ManyToManyField(
        ContactPersonEggs, related_name="contact_person_seller",
        blank=True,
    )
    manager = models.ForeignKey(
        CustomUser, related_name='seller_manager',
        verbose_name='Менеджер',
        on_delete=models.SET_NULL, null=True,
    )
    guest = models.ForeignKey(
        CustomUser, related_name='guest_manager_seller',
        verbose_name='Гость-Менеджер',
        on_delete=models.SET_NULL, null=True, blank=True,
        validators=[validate_guest_role],
    )
    entitys = models.ManyToManyField(
        EntityEggs,
        related_name="client_seller",
        blank=True,
    )

    def __str__(self):
        if self.requisites:
            return f'Продавец {self.requisites.name}'
        else:
            return f'Продавец/{self.inn}'


class LogicCardEggs(LogicCard):

    class Meta:
        db_table = 'LogicCardEggs'
        verbose_name = 'Перевозчик'
        verbose_name_plural = 'Перевозчики'
        ordering = ['inn']

    region = models.CharField(
        max_length=100, verbose_name='Регион',
    )
    requisites = models.ForeignKey(
        RequisitesEggs, on_delete=models.PROTECT,
        verbose_name='Реквизиты', null=True, blank=True,
    )
    documents_contract = models.OneToOneField(
        DocumentsContractEggsModel, on_delete=models.PROTECT,
        verbose_name='Документы (Договора)', null=True,
    )
    contact_person = models.ManyToManyField(
        ContactPersonEggs, related_name="contact_person_logic",
        blank=True,
    )
    guest = models.ForeignKey(
        CustomUser, related_name='guest_manager_logic',
        verbose_name='Гость-Менеджер',
        on_delete=models.SET_NULL, null=True
    )
    manager = models.ForeignKey(
        CustomUser, related_name='logic_manager',
        verbose_name='Менеджер',
        on_delete=models.SET_NULL, null=True
    )
    entitys = models.ManyToManyField(
        EntityEggs,
        related_name="client_logic",
        blank=True,
    )

    def __str__(self):
        if self.requisites:
            return f'Перевозчик {self.requisites.name}'
        else:
            return f'Перевозчик/{self.inn}'
