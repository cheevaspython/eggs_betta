from django.db import models

from users.models import CustomUser


class AbstractApplication(models.Model):
    class Meta:
        abstract = True

    delivery_window_from = models.DateField(
        verbose_name='Окно поставки от', null=True, blank=True
    )
    delivery_window_until = models.DateField(
        verbose_name='Окно поставки до', null=True, blank=True
    )
    created_date_time = models.DateTimeField(
        auto_now_add=True, verbose_name='Создана'
    )
    edited_date_time = models.DateTimeField(
        auto_now=True, verbose_name='Изменена'
    )
    is_active = models.BooleanField(
        editable=True, default=True, verbose_name='Активна'
    )
    owner = models.ForeignKey(
        CustomUser, verbose_name='Автор заявки',
        on_delete=models.SET_NULL, null=True
    )
    comment = models.CharField(
        max_length=255, verbose_name='Комментарий', null=True, blank=True
    )
    region = models.CharField(
        max_length=50, verbose_name='Регион', null=True, blank=True
    )

