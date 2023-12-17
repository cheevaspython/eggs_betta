from general_layout.deal.models.additional_expense import AdditionalExpense

from product_eggs.tasks.deal_pay_change import task_calc_margin


class AdditionalExpenseEggs(AdditionalExpense):

    class Meta:
        db_table = 'additional_expense'
        verbose_name = 'Доп Расход'
        verbose_name_plural = 'Доп Расход'
        ordering = ['pk']

    def save(self, *args, **kwargs):
        self.expense_total = (
          self.expense_total_form_1 +
          self.expense_total_form_2
        )
        super().save(*args, **kwargs)
        task_calc_margin(self)

    def __str__(self):
        return 'Доп Расход'

