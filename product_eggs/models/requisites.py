from general_layout.bases.models import Requisites


class RequisitesEggs(Requisites):

    class Meta:
        db_table = 'RequisitesEggs'
        verbose_name = 'Реквизиты'
        verbose_name_plural = 'Реквизиты'
        ordering = ['pk']

    def __str__(self):
        return f'Реквизиты {self.inn}'
