from django.db import models
from django.core import validators


class ContactPerson(models.Model):

    class Meta:
        abstract = True

    name = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Контактное лицо',
    )
    email = models.EmailField(
        blank=True, null=True, unique=True,
        max_length=50, verbose_name='Почта контактно лицо',
    )
    phone1 = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name='Номер телефона контактного лица 1', unique=True,
        validators=[validators.MaxLengthValidator(11)],
    )
    phone2 = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name='Номер телефона контактного лица 2', unique=True,
        validators=[validators.MaxLengthValidator(11)],
    )
    phone3 = models.CharField(
        max_length=20, blank=True, null=True,
        verbose_name='Номер телефона контактного лица 3', unique=True,
        validators=[validators.MaxLengthValidator(11)],
    )
    info = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name='Дополнительная информация',
    )

