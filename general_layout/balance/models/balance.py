from django.db import models

from product_eggs.services.validation.validate_fields import validate_value_by_positive


class BalanceBaseClient(models.Model):

    class Meta:
        abstract = True

    pay_limit = models.BigIntegerField(
        default=0,
        verbose_name='Лимит задолженности',
        validators=[validate_value_by_positive],
    )
    pay_limit_cash = models.BigIntegerField(
        default=0,
        verbose_name='Лимит задолженности, нал',
        validators=[validate_value_by_positive],
    )
    balance = models.FloatField(
        default=0,
        verbose_name='Баланс',
    )
    balance_form_one = models.FloatField(
        default=0,
        verbose_name='Баланс по форме 1',
    )
    balance_form_two = models.FloatField(
        default=0,
        verbose_name='Баланс по форме 2',
    )


