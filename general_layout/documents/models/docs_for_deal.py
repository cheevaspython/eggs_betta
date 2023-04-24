from datetime import datetime

from django.db import models


class DocumentsDealModel(models.Model):

    class Meta:
        abstract = True

    data_number_json = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='Даты и номера форма 1',
    )
    data_number_json_cash = models.JSONField(
        blank=True, null=True, 
        default=dict, verbose_name='Даты и номера форма 2',
    )
    tmp_json = models.JSONField(
        blank=True, null=True,
        default=dict, verbose_name='temp json',
    )
    payment_for_contract = models.BooleanField(
        editable=True, default=False, verbose_name='Оплата по основному договору',
    )
    deal_docs_links_json = models.JSONField(
        blank=True, null=True,
        default=dict, verbose_name='deal_docs_dict_json',
    )
    payment_order_incoming = models.FileField(
        blank=True, null=True, 
        upload_to=(f'uploads/deal_docs/payment_order_incoming/{datetime.today().year}/{datetime.today().month}/' + 
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Входящее платежное поручение',
    )
    payment_order_outcoming = models.FileField(
        blank=True, null=True, 
        upload_to=(f'uploads/deal_docs/payment_order_outcoming/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Исходящее платежное поручение',
    )
    payment_order_outcoming_logic = models.FileField(
        blank=True, null=True, 
        upload_to=(f'uploads/deal_docs/payment_order_outcoming_logic/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Исходящее платежное поручение логистика',
    )
    specification_seller = models.FileField(
        blank=True, null=True, 
        upload_to=(f'uploads/deal_docs/specification_seller/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Спецификация от продавца',
    )
    account_to_seller = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/account_to_seller/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Счет на оплату продавцу',
    )
    specification_buyer = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/specification_buyer/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Спецификация от покупателя',
    )
    account_to_buyer = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/account_to_buyer/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Счет на оплату покупателю',
    )
    application_contract_logic = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/application_contract_logic/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Договор-заявка на транспорт',
    )
    account_to_logic = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/account_to_logic/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Счет на транспорт',
    )
    UPD_incoming = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/UPD_incoming/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Входящая УПД',
    )
    account_invoicing_from_seller = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/account_invoicing_from_seller/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Счет-Фактура от продавца',
    )
    product_invoice_from_seller = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/product_invoice_from_seller/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Товарная накладная от продавца',
    )
    UPD_outgoing = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/UPD_outgoing/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Исходящая УПД',
    )
    account_invoicing_from_buyer = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/account_invoicing_from_buyer/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Счет-Фактура от покупателя',
    )
    product_invoice_from_buyer = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/product_invoice_from_buyer/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Товарная накладная от покупателя',
    )
    veterinary_certificate_buyer = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/veterinary_certificate_buyer/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Ветеринарное свидетельство от покупателя',
    )
    veterinary_certificate_seller = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/veterinary_certificate_seller/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Ветеринарное свидетельство от продавца',
    )
    international_deal_CMR = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/international_deal_CMR/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Международная сделка, ЦМР',
    )
    international_deal_TTN = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/international_deal_TTN/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Международная сделка, ТТН',
    )
    UPD_logic = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/UPD_logic/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Транспортная УПД',
    )
    account_invoicing_logic = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/account_invoicing_logic/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Транспортная счет-фактура',
    )
    product_invoice_logic = models.FileField(
        blank=True, null=True,
        upload_to=(f'uploads/deal_docs/product_invoice_logic/{datetime.today().year}/{datetime.today().month}/' +
            f'{datetime.today().day}/{datetime.today().hour}-{datetime.today().minute}-{datetime.today().second}/'), 
        verbose_name='Транспортная товарная накладная',
    )
     

 










