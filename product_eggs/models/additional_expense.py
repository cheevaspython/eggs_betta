from general_layout.deal.models.additional_expense import AdditionalExpense


class AdditionalExpenseEggs(AdditionalExpense):

    class Meta:
        db_table = 'additional_expense'
        verbose_name = 'Доп Расход'
        verbose_name_plural = 'Доп Расход'
        ordering = ['pk']

    def __str__(self):
        return 'Доп Расход'
