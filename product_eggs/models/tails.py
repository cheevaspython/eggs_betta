from general_layout.tails.tail_client import TailsContragentModel
from product_eggs.tasks import change_client_balance_tail


class TailsContragentModelEggs(TailsContragentModel):

    class Meta:
        db_table = 'TailsContragentModelEggs'
        verbose_name = 'Депозит'
        verbose_name_plural = 'Депозиты'
        ordering = ['pk']
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            change_client_balance_tail(self.pk)
        except Exception as e:
            print(e) #TODO logging
    
    def __str__(self):
        return f'Депозит № {self.pk}'



