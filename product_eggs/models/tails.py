from general_layout.tails.tail_client import TailsContragentModel


class TailsContragentModelEggs(TailsContragentModel):

    class Meta:
        db_table = 'TailsContragentModelEggs'
        verbose_name = 'Депозит'
        verbose_name_plural = 'Депозиты'
        ordering = ['pk']
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    # def save(self, *args, **kvargs):
    #     from product_eggs.tasks import change_client_balance_tail
    #
    #     if delta_one := self.current_tail_form_one != self.__current_tail_form_one:
    #         change_client_balance_tail(self.pk, delta_one)
    #     elif delta_two := self.current_tail_form_two != self.__current_tail_form_two:
    #         change_client_balance_tail(self.pk, delta_two, form_one=False)
    #
    #     super(TailsContragentModelEggs, self).save(*args, **kvargs)
    #
    def __str__(self):
        return f'Депозит № {self.pk}'



