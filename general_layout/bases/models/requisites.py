from django.db import models
from django.core import validators

from product_eggs.services.validation.validate_fields import validate_inn, validate_for_letters


class Requisites(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Название',
    )
    inn = models.CharField(
        max_length=13, verbose_name='ИНН',
        validators=[validate_inn],
        primary_key=True,
    )
    kpp = models.CharField(
        max_length=9,
        null=True,
        blank=True,
        verbose_name='КПП',
        validators=[
            validators.MaxLengthValidator(9),
            validators.MinLengthValidator(9),
            validate_for_letters,
        ],
    )
    region = models.CharField(
        max_length=50, verbose_name='Регион',
        null=True, blank=True,
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Страна',
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Город',
    )
    site = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Доменное имя сервера',
    )
    phone = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name='Номер телефона', unique=True,
        validators=[validators.MaxLengthValidator(11)],
    )
    phone_with_out_code = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name='Номер телефона без кода',
    )
    phone2 = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name='Номер телефона 2', unique=True,
        validators=[validators.MaxLengthValidator(11)],
    )
    phone3 = models.CharField(
        blank=True,
        null=True,
        max_length=20,
        verbose_name='Номер телефона 3', unique=True,
        validators=[validators.MaxLengthValidator(11)],
    )
    general_manager = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Генеральный директор',
    )
    email = models.EmailField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Почта', unique=True,
    )
    email2 = models.EmailField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Почта', unique=True,
    )
    email3 = models.EmailField(
        blank=True,
        null=True,
        max_length=100,
        verbose_name='Почта', unique=True,
    )
    bank_name = models.CharField(
        max_length=255,
        null=True,
        blank=True, verbose_name='Название банка',
    )
    register_date = models.CharField(
        max_length=100,
        null=True,
        blank=True, verbose_name='Дата регистрации',
    )
    bic_bank = models.CharField(
        max_length=9,
        null=True,
        blank=True,
        verbose_name='БИК банка',
        validators=[validators.MaxLengthValidator(9),
        validators.MinLengthValidator(9)],
    )
    cor_account = models.CharField(
        max_length=20, null=True, blank=True,
        verbose_name='Кор счет банка',
        validators=[
            validators.MaxLengthValidator(20),
            validators.MinLengthValidator(20),
            validate_for_letters,
        ],
    )
    customers_pay_account = models.CharField(
        max_length=20, null=True, blank=True,
        verbose_name='Счет клиента', unique=True,
        validators=[
            validators.MaxLengthValidator(20),
            validators.MinLengthValidator(20),
            validate_for_letters,
        ],
    )
    legal_address = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Юридический адресс', unique=True,
    )
    physical_address = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Фактический адресс',
    )
    mail_address = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Почтовый адресс',
    )
