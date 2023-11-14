from django.db import models

from general_layout.bases.models.abstract_client_card import AbstractClientCard
from product_eggs.services.validation.validate_fields import validate_inn


class LogicCard(AbstractClientCard):

    class Meta:
        abstract = True

    inn = models.CharField(
        max_length=13, verbose_name='ИНН / Паспорт',
        validators=[validate_inn],
        primary_key=True,
    )
    contact_person = models.CharField(
        max_length=255, blank=True,
        null=True, verbose_name='Контактное лицо'
    )
    comment = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name='Дополнительная информация'
    )
    # rating = None

