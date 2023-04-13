from django.db import models

from users.models import CustomUser
from general_layout.application.models.abstract_app import AbstractApplication
from general_layout.bases.models.seller_card import SellerCard


class ApplicationFromSellerBase(AbstractApplication):

    class Meta:
        abstract = True

    current_seller = models.ForeignKey(
        SellerCard, on_delete=models.PROTECT, verbose_name='Продавец'
    )
    owner = models.ForeignKey(
        CustomUser, related_name='app_from_seller',
        verbose_name='Автор заявки от продавца', on_delete=models.SET_NULL,
        null=True
    )
    def __str__(self):
        return f'{self.current_seller.name}, заявка продавца №{self.pk}'
