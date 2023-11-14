from general_layout.comments.models.comments import Comments


class CommentEggs(Comments):

    class Meta:
        db_table = 'comments_eggs'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pk']

    def __str__(self):
        return f'Комментарий №{self.pk}'

