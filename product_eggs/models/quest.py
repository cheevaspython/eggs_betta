from general_layout.deal.models.quest import Quest


class QuestEggs(Quest):

    class Meta:
        db_table = 'quest_eggs'
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['pk']

    def __str__(self):
        return f'Задача №{self.pk}'

