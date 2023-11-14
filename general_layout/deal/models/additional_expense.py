from django.db import models


class AdditionalExpense(models.Model):

    class Meta:
        abstract = True

    expense_total = models.FloatField(
        verbose_name='Доп Расход', default=0,
    )
    expense_detail_json = models.JSONField(
        blank=True,
        default=dict, verbose_name='Доп Расход: детали'
    )
    tmp_json = models.JSONField(
        blank=True,
        default=dict, verbose_name='tmp_json for change'
    )

