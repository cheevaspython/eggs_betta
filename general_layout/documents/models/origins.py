from django.db import models


class OriginsDeal(models.Model):

    STATUS = (
		(1, 'Отсутствует'),
		(2, 'Получен'),
		(3, 'Передан по ЭДО'),
		(4, 'Несущественно'),
	)
    class Meta:
        abstract = True

    payment_order= models.PositiveSmallIntegerField(
    	choices=STATUS, default=1, 
        verbose_name='платежное поручение')
    specification_seller = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1, 
        verbose_name='Спецификация от продавца')
    account_to_seller = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1, 
        verbose_name='Счет на оплату продавцу')
    specification_buyer = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1, 
        verbose_name='Спецификация от покупателя')
    account_to_buyer = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,  
        verbose_name='Счет на оплату покупателю')
    application_contract_logic = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1, 
        verbose_name='Договор-заявка на транспорт')
    account_to_logic = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,  
        verbose_name='Счет на транспорт')
    UPD_incoming = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1, 
        verbose_name='Входящая УПД')
    account_invoicing_from_seller = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1, 
        verbose_name='Счет-фактура от продавца')
    product_invoice_from_seller = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Товарная накладная от продавца')
    UPD_outgoing = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Исходящая УПД')
    account_invoicing_from_buyer = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Счет-фактура от покупателя')
    product_invoice_from_buyer = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Товарная накладная от покупателя')
    veterinary_certificate_buyer = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Ветеринарное свидетельство от покупателя')
    veterinary_certificate_seller = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Ветеринарное свидетельство от продавца')
    international_deal_CMR = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Международная сделка, ЦМР')
    international_deal_TTN = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Международная сделка, ТТН')
    UPD_logic = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Транспортная УПД')
    account_invoicing_logic = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Транспортная счет-фактура')
    product_invoice_logic = models.PositiveSmallIntegerField(
    	choices=STATUS, default=1,
        verbose_name='Транспортная товарная накладная')
    

