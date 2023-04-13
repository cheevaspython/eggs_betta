from django.db import models

from general_layout.bases.models import AbstractClientCard


class BuyerCard(AbstractClientCard):

    class Meta:
        abstract = True

    buy_limit = models.BigIntegerField(
        null=True, blank=True, default=0, verbose_name='Лимит максимальной задолженности'            
    )
    current_debt = models.BigIntegerField(
        null=True, blank=True, default=0, verbose_name='Текущая задолженность' 
    )

