from datetime import date

from django.db import models
 

class DocumentsContragentModel(models.Model):

    class Meta:
        abstract = True

    contract = models.FileField(
        blank=True, null=True, 
        upload_to=f'uploads/contragents_docs/contracts/{date.today().year}/{date.today().month}/{date.today().day}/', 
        verbose_name='Договор'
    )
    contract_links_dict_json = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='contract_links',
    )
    multi_pay_order = models.FileField(
        blank=True, null=True, 
        upload_to=f'uploads/contragents_docs/multy_pay_order/{date.today().year}/{date.today().month}/{date.today().day}/', 
        verbose_name='ПП на несколько сделок',
    )
    multi_pay_order_links_dict_json = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='multy_pay_order_links',
    )
    tmp_json_for_multi_pay_order = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='tmp_json_for_multy_pay_order',
    )
    data_number_json = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='Даты и номера форма 1',
    )
    data_number_json_cash = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='Даты и номера форма 2',
    )
    multy_pay_json = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='multy_pay_json', 
    )
    cash_docs = models.FileField(
        blank=True, null=True, 
        upload_to=f'uploads/contragents_docs_cash/{date.today().year}/{date.today().month}/{date.today().day}/', 
        verbose_name='Покупатель доки наличка'
    )
    cash_docs_links_dict_json = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='links_buyer_cash'
    )



