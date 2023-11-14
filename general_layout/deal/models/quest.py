from django.db import models

from product_eggs.models.base_deal import BaseDealEggsModel
from users.models import CustomUser


class Quest(models.Model):

    class Meta:
        abstract = True

    quest_task_text = models.TextField(
        verbose_name='Текст задачи',
        null=True, blank=True,
    )
    quest_base_model = models.ForeignKey(
        BaseDealEggsModel,
        related_name='base_deal_model_for_quest',
        on_delete=models.SET_NULL, null=True
    )
    quest_to_user = models.ForeignKey(
        CustomUser, related_name='quest_to',
        on_delete=models.SET_NULL, null=True
    )
    owner = models.ForeignKey(
        CustomUser, verbose_name='Автор задачи',
        on_delete=models.SET_NULL, null=True,
    )
    is_actual = models.BooleanField(
        editable=True, default=True,
        verbose_name='Актуальна',
    )
    is_active = models.BooleanField(
        editable=True, default=True,
        verbose_name='Активна',
    )
    created_date_time = models.DateTimeField(
        auto_now_add=True, verbose_name='Создана',
    )
    edited_date_time = models.DateTimeField(
        auto_now=True, verbose_name='Изменена',
    )
    not_read = models.BooleanField(
        editable=True, default=True,
        verbose_name='not_read'
    )
    done = models.BooleanField(
        editable=True, default=False,
        verbose_name='done'
    )
    info = models.BooleanField(
        editable=True, default=False,
        verbose_name='info'
    )

    def __str__(self):
        return f'Задача для {self.quest_to_user}'
