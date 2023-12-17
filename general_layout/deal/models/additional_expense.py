from django.db import models


class AdditionalExpense(models.Model):

    class Meta:
        abstract = True

    logic_pay = models.FloatField(
        verbose_name='Оплата логисту',
        default=0,
    )
    logic_name = models.CharField(
        verbose_name='Имя логиста',
        max_length=25,
        blank=True, null=True,
    )
    expense_total = models.FloatField(
        verbose_name='Доп Расход',
        default=0,
    )
    expense_total_form_1 = models.FloatField(
        verbose_name='Доп Расход по форме 1',
        default=0,
    )
    expense_total_form_2 = models.FloatField(
        verbose_name='Доп Расход по форме 2',
        default=0,
    )
    expense_detail_json = models.JSONField(
        blank=True,
        default=dict,
        verbose_name='Доп Расход: детали'
    )
    tmp_json = models.JSONField(
        blank=True,
        default=dict,
        verbose_name='tmp_json for change'
    )
    tmp_multi_json = models.JSONField(
        blank=True,
        default=dict,
        verbose_name='tmp_multi_json for change'
    )

