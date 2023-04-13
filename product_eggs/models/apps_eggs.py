from django.db import models

from general_layout.application.models import AbstractApplication
from product_eggs.models.base_eggs import SellerCardEggs, BuyerCardEggs


class AbstractApplicationEggs(AbstractApplication):

    class Meta:
        abstract = True

    cB = models.PositiveIntegerField(
        verbose_name='Яйца СВ, в десятках:',     
        default=0,
    )
    c0 = models.PositiveIntegerField(
        verbose_name='Яйца С0, в десятках:',
        default=0,
    )
    c1 = models.PositiveIntegerField(
        verbose_name='Яйца С1, в десятках:',     
        default=0,
    )
    c2 = models.PositiveIntegerField(
        verbose_name='Яйца С2, в десятках:',
        default=0,
    )
    c3 = models.PositiveIntegerField(
        verbose_name='Яйца С3, в десятках:',
        default=0,
    )
    dirt = models.PositiveIntegerField(
        verbose_name='Грязь, в десятках:',
        default=0,
    )


class ApplicationFromBuyerBaseEggs(AbstractApplicationEggs):
    
    class Meta:
        db_table = 'ApplicationFromBuyerBaseEggs'
        verbose_name = 'Заявка от покупателя'
        verbose_name_plural = 'Заявки от покупателя'
        ordering = ['pk']

    current_buyer = models.ForeignKey(
        BuyerCardEggs, on_delete=models.PROTECT, verbose_name='Покупатель'
    )
    cB_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c0_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c1_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0
    )
    c2_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c3_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    dirt_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    unloading_address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Адрес разгрузки',
    )
    postponement_pay = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Отсрочка оплаты',
        default=0,
    )

    def __str__(self):
        return f'Заявка покупателя №{self.pk}'


class ApplicationFromSellerBaseEggs(AbstractApplicationEggs):

    class Meta:
        db_table = 'ApplicationFromSellerBaseEggs'
        verbose_name = 'Заявка от продавца'
        verbose_name_plural = 'Заявки от продавца'
        ordering = ['pk']

    current_seller = models.ForeignKey(
        SellerCardEggs, on_delete=models.PROTECT, verbose_name='Продавец'
    )
    cB_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c0_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c1_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0
    )
    c2_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    c3_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    dirt_cost = models.FloatField(
        verbose_name='Стоимость за десяток', default=0,
    )
    loading_address = models.CharField(
        max_length=255, blank=True, null=True, verbose_name='Адрес погрузки',
    )
    files_upload = models.FileField(
        blank=True, null=True,
        upload_to='uploads/', verbose_name='Подгружаемые документы',
    )
    pre_payment_application = models.BooleanField(
        editable=True, default=True, verbose_name='Предоплата',
    )
    import_application = models.BooleanField(
        editable=True, default=False, verbose_name='Импорт',
    )
    postponement_pay = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Отсрочка оплаты',
        default=0,
    )
    def __str__(self):
        return f'Заявка продавца №{self.pk}'
     


