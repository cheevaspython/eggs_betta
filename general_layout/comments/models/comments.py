from django.db import models


class Comments(models.Model):

    class Meta:
        abstract = True

    created_date_time = models.DateTimeField(
        auto_now_add=True, verbose_name='Создана',
    )
    edited_date_time = models.DateTimeField(
        auto_now=True, verbose_name='Изменена',
    )
    comment_body_json = models.JSONField(
        blank=True,
        default=dict, verbose_name='Сообщение'
    )
    logs = models.JSONField(
        blank=True,
        default=dict, verbose_name='logs'
    )
    tmp_json = models.JSONField(
        blank=True,
        default=dict, verbose_name='tmp_json'
    )
    is_active = models.BooleanField(
        editable=True, default=True,
        verbose_name='Активна',
    )

