from datetime import date

from django.db import models
 

class DocumentsBuyerModel(models.Model):

    class Meta:
        abstract = True
    
    buyer_cash_docs = models.FileField(
        blank=True, null=True, 
        upload_to=f'uploads/buyer_cash_docs/{date.today().year}/{date.today().month}/{date.today().day}/', 
        verbose_name='Покупатель доки наличка'
    )
    cash_links_dict_json = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='links_buyer_cash'
    )
    data_number_json = models.JSONField(
        default=dict, null=True, blank=True,
        verbose_name='Покупатель наличка: детали',
    )
    tmp_json = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='temp json',
    )

