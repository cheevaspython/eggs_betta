from general_layout.tails.tail_client import TailsContragentModel


class TailsContragentModelEggs(TailsContragentModel):

    class Meta:
        db_table = 'TailsContragentModelEggs'
        verbose_name = 'Депозит'
        verbose_name_plural = 'Депозиты'
        ordering = ['pk']
    
    def __str__(self):
        return f'Депозит № {self.pk}'



