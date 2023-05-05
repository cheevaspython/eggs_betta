from django.db import models

from general_layout.documents.models.docs_for_deal import DocumentsDealModel
from general_layout.documents.models.docs_for_contragent import DocumentsContragentModel

from product_eggs.models.origins import OriginsDealEggs


class DocumentsDealEggsModel(DocumentsDealModel):

    class Meta:
        db_table = 'DocumentsDealEggs'
        verbose_name = 'Документы по сделке'
        verbose_name_plural = 'Документы по сделке'
        ordering = ['pk']

    origins = models.OneToOneField(OriginsDealEggs, on_delete=models.PROTECT, 
        verbose_name='Оригиналы документов', null=True)

    def __str__(self):
        return f'Документы по сделке {self.pk}'


class DocumentsContractEggsModel(DocumentsContragentModel):

    class Meta:
        db_table = 'DocumentsConteragentsEggs'
        verbose_name = 'Документы по контрагенту'
        verbose_name_plural = 'Документы по контрагенту'
        ordering = ['pk']

    def __str__(self):
        return f'Документы по контрагенту {self.pk}'


