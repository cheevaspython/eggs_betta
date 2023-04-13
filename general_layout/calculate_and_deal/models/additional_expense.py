from django.db import models


class AdditionalExpense(models.Model):

    class Meta:
        abstract = True

    expense_total = models.FloatField(
        verbose_name='Доп Расход', default=0,
    )
    expense_detail_json = models.JSONField(
        default=dict, verbose_name='Доп Расход: детали'
    )

