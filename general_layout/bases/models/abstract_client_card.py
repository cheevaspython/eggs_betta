from django.db import models
from django.core import validators


class AbstractClientCard(models.Model):

    class Meta:
        abstract = True

    inn = models.CharField(
        max_length=12, verbose_name='ИНН',
        validators=[
            validators.MaxLengthValidator(12),
            validators.MinLengthValidator(10)
        ],
        primary_key=True,
    )
    comment = models.CharField(
        max_length=255,
        verbose_name='Дополнительная информация',
        null=True, blank=True,
    )
    resident = models.BooleanField(
        blank=True, null=True,
        editable=True, default=True,
        verbose_name='Резидент',
    )
    link = models.CharField(
        max_length=255, verbose_name='Ссылка',
        null=True, blank=True,
    )
    is_active = models.BooleanField(
        editable=True, default=True,
        verbose_name='Активна',
    )

    def __str__(self):
        return f'{self.inn}'


class AbstractAddressCard(models.Model):

    class Meta:
        abstract = True

    prod_address_1 = models.CharField(
        max_length=254, verbose_name='Адрес производства',
    )
    prod_address_2 = models.CharField(
        max_length=254, blank=True, null=True, verbose_name='Адрес производства',
    )
    prod_address_3 = models.CharField(
        max_length=254, blank=True, null=True, verbose_name='Адрес производства',
    )
    prod_address_4 = models.CharField(
        max_length=254, blank=True, null=True, verbose_name='Адрес производства',
    )
    prod_address_5 = models.CharField(
        max_length=254, blank=True, null=True, verbose_name='Адрес производства',
    )
    prod_address_6 = models.CharField(
        max_length=254, blank=True, null=True, verbose_name='Адрес производства',
    )
    prod_address_7 = models.CharField(
        max_length=254, blank=True, null=True, verbose_name='Адрес производства',
    )
    prod_address_8 = models.CharField(
        max_length=254, blank=True, null=True, verbose_name='Адрес производства',
    )
    prod_address_9 = models.CharField(
        max_length=254, blank=True, null=True, verbose_name='Адрес производства',
    )
    prod_address_10 = models.CharField(
        max_length=254, blank=True, null=True, verbose_name='Адрес производства',
    )


class AbstractWarehouseCard(models.Model):

    class Meta:
        abstract = True

    warehouse_address_1 = models.CharField(
        max_length=255, verbose_name='Адрес склада',
    )
    warehouse_address_2 = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Адрес склада',
    )
    warehouse_address_3 = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Адрес склада',
    )
    warehouse_address_4 = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Адрес склада',
    )
    warehouse_address_5 = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Адрес склада',
    )
    warehouse_address_6 = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Адрес склада',
    )
    warehouse_address_7 = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Адрес склада',
    )
    warehouse_address_8 = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Адрес склада',
    )
    warehouse_address_9 = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Адрес склада',
    )
    warehouse_address_10 = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Адрес склада',
    )




