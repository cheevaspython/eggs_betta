from django.db import models

from general_layout.calculate_and_deal.models import ConfirmedCalculate
from users.models import CustomUser


class Deal(models.Model):
    
	class Meta:
		abstract = True

	confirmed_calculate = models.OneToOneField(
	    ConfirmedCalculate, on_delete=models.PROTECT,
	    verbose_name='Просчет подтвержденный', null=True,
	)
	STATUS = (
		(1, 'на подтверждении у фин. директора'),
		(2, 'на ожидании основания платежа от продавца'),
		(3, 'на подтверждении у фин. директора (по оплате счета от продавца'),
		(4, 'на ожидании оплаты и загрузки бухгалтером счета от продавца'),
		(5, 'на погрузке и ожидании УПД от продавца'),
		(6, 'товар в пути, ожидаем запрос на исходящую УПД'),
		(7, 'на ожидании загрузки исходящей УПД бухгалтером'),
		(8, 'на разгрузке, ожидаем подписанную УПД'),
		(9, 'на ожидании закрывающих документов'),
	)
	status = models.PositiveSmallIntegerField(
		choices=STATUS, default=1
	)
	processing_to_confirm = models.BooleanField(
		editable=True, default=True, verbose_name='processing_to_confirm'
	)
	is_active = models.BooleanField(
		editable=True, default=True, verbose_name='is_active'
	)
	upd_1 = models.FileField(
	    upload_to='uploads/%Y/%m/%d/', blank=True, null=True, verbose_name='UPD 1'
	)
	upd_2 = models.FileField(
	    upload_to='uploads/%Y/%m/%d/', blank=True, null=True, verbose_name='UPD 2'
	)
	created = models.DateTimeField(
	    auto_now_add=True, verbose_name='Создана'
	)
	edited = models.DateTimeField(
	    auto_now=True, verbose_name='Изменена'
	)
	owner = models.ForeignKey(
		CustomUser, related_name='owner', on_delete=models.SET_NULL, null=True
	)

	def __str__(self):
	    return f'Сделка №{self.pk}'

