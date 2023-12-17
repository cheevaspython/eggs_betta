from django.db import models


class PersonalSalaryBalance(models.Model):

    class Meta:
        abstract = True

    wage_balance = models.FloatField(
        verbose_name='Текущий баланс',
        default=0,
    )
    get_wage_dict = models.JSONField(
        blank=True,
        default=dict,
        verbose_name='Таблица получения средств из кассы',
    )
    month_hash_dict = models.JSONField(
        blank=True,
        default=dict,
        verbose_name='Таблица значений на 1ое',
    )
