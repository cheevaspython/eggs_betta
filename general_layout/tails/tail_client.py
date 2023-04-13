from django.db import models
 

class TailsContragentModel(models.Model):

    class Meta:
        abstract = True

    current_tail_form_one = models.FloatField(
        default=0, null=True, blank=True,
        verbose_name='Депозит',
    )
    current_tail_form_two = models.FloatField(
        default=0, null=True, blank=True,
        verbose_name='Депозит нал',
    )
    active_tails_form_one = models.IntegerField(
        default=0, null=True, blank=True,
        verbose_name='active_tails_form_one',
    )
    active_tails_form_two = models.IntegerField(
        default=0, null=True, blank=True,
        verbose_name='active_tails_form_two',
    )
    tail_dict_json = models.JSONField(
        null=True, blank=True,
        default=dict, verbose_name='tail_dict_json', 
    )
    tail_dict_json_cash = models.JSONField(
        null=True, blank=True,
        default=dict, verbose_name='tail_dict_json_cash', 
    )
