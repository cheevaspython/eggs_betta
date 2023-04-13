from django.db import models
from django.core import validators


class AbstractClientCard(models.Model):
    PAY_TYPE = ((1, 'С  НДС'), (2, 'Без НДС'), (3, 'Наличка'))
    
    class Meta:
        abstract = True

    name = models.CharField(
        max_length=255, unique=True, verbose_name='Название', 
    )
    inn = models.CharField(
        max_length=12, verbose_name='ИНН',   
        validators=[validators.MaxLengthValidator(12), validators.MinLengthValidator(10)],
        primary_key=True,
    )
    general_manager = models.CharField(
        max_length=255, verbose_name='Генеральный директор', 
    )
    phone = models.CharField(
        max_length=20, verbose_name='Номер телефона', unique=True,
        validators=[validators.MaxLengthValidator(11)],
    )
    email = models.EmailField(
        max_length=50, verbose_name='Почта', unique=True,
    )
    pay_type = models.PositiveSmallIntegerField(
        verbose_name='Тип оплаты', choices=PAY_TYPE, null=True, blank=True,
    )
    comment = models.CharField(
        max_length=255, verbose_name='Дополнительная информация', null=True, blank=True,
    )
    contact_person = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Контактное лицо',
    )
    region = models.CharField(
        max_length=100, verbose_name='Регион',
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




