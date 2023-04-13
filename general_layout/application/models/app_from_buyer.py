from django.db import models

from users.models import CustomUser
from general_layout.application.models import AbstractApplication
from general_layout.bases.models import BuyerCard


class ApplicationFromBuyerBase(AbstractApplication):

    class Meta:
        abstract = True

    current_buyer = models.ForeignKey(
        BuyerCard, on_delete=models.PROTECT, verbose_name='Покупатель'
    )
    owner = models.ForeignKey(
        CustomUser, related_name='app_from_buyer',
        verbose_name='Автор заявки от покупателя', on_delete=models.SET_NULL,
        null=True
    )
    def __str__(self):
        return f'{self.current_buyer.name}, заявка покупателя №{self.pk}'
