from django.db import models


class TailsContragentModel(models.Model):

    class Meta:
        abstract = True

    current_tail_form_one = models.FloatField(
        default=0,
        verbose_name='Депозит',
    )
    current_tail_form_two = models.FloatField(
        default=0,
        verbose_name='Депозит нал',
    )
    active_tails_form_one = models.IntegerField(
        default=0,
        verbose_name='active_tails_form_one',
    )
    active_tails_form_two = models.IntegerField(
        default=0,
        verbose_name='active_tails_form_two',
    )
    data_number_json = models.JSONField(
        blank=True,
        default=dict, verbose_name='tail_dict_json',
    )
    data_number_json_cash = models.JSONField(
        blank=True,
        default=dict, verbose_name='tail_dict_json_cash',
    )
    multi_tails = models.JSONField(
        blank=True,
        default=dict, verbose_name='multi_tails',
    )
