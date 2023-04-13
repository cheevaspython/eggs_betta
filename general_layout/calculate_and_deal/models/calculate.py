from django.db import models

from users.models import CustomUser
from general_layout.application.models import ApplicationFromBuyerBase
from general_layout.application.models import ApplicationFromSellerBase


class Calculate(models.Model):

    class Meta:
        abstract = True

    application_from_buyer = models.ForeignKey(
        ApplicationFromBuyerBase, on_delete=models.PROTECT, verbose_name='Заявка от продавца'
    )
    application_from_seller = models.ForeignKey(
        ApplicationFromSellerBase, on_delete=models.PROTECT, verbose_name='Заявка от покупателя'
    )
    average_delivery_cost = models.PositiveIntegerField(
        verbose_name='Средняя стоимость доставки'
    )
    owner = models.ForeignKey(
        CustomUser, related_name='calculate', verbose_name='Автор просчета', on_delete=models.SET_NULL, null=True
    )
    is_active = models.BooleanField(
        editable=True, default=True, verbose_name='is_active'
    )
    def __str__(self):
        return f'Просчет №{self.pk}'
