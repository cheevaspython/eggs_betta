from general_layout.documents.models.origins import OriginsDeal


class OriginsDealEggs(OriginsDeal):

    class Meta:
        db_table = 'OriginsDealEggs'
        verbose_name = 'Оригиналы'
        verbose_name_plural = 'Оригиналы'
        ordering = ['pk']

    def __str__(self):
        return 'Оригиналы'

