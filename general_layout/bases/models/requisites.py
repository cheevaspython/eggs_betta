from django.db import models
from django.core import validators


class Requisites(models.Model):

    class Meta:
        abstract = True

    general_manager = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Генеральный директор',
    )
    inn = models.CharField(
        max_length=12, verbose_name='ИНН',   
        validators=[validators.MaxLengthValidator(12), validators.MinLengthValidator(10)],
        primary_key=True,
    )
    bank_name = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Название банка',
    )
    bic_bank = models.CharField(
        max_length=9, null=True, blank=True, verbose_name='БИК банка',
        validators=[validators.MaxLengthValidator(9), validators.MinLengthValidator(9)],
    )
    cor_account = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='Кор счет банка',
        validators=[validators.MaxLengthValidator(20), validators.MinLengthValidator(20)],
    )
    customers_pay_account = models.CharField(
        max_length=20, null=True, blank=True, verbose_name='Счет клиента', unique=True,
        validators=[validators.MaxLengthValidator(20), validators.MinLengthValidator(20)],
    ) 
    legal_address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Юридический адресс', unique=True,
    )
    physical_address = models.CharField(
        max_length=255, null=True, blank=True, verbose_name='Фактический адресс',
    )
