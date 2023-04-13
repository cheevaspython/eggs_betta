from django.db import models

from users.models import CustomUser
from general_layout.calculate_and_deal.models import Calculate

from general_layout.bases.models import LogicCard


class ConfirmedCalculate(models.Model):
	
	class Meta:
		abstract = True

	current_calculate = models.ForeignKey(
		Calculate, on_delete=models.PROTECT,
		verbose_name='Просчет', null=True, blank=True
	)
	current_logic = models.ForeignKey(
		LogicCard, on_delete=models.PROTECT,
		blank=True, null=True, verbose_name='Логист'
	)
	delivery_date_from_seller = models.DateField(
		verbose_name='Дата погрузки', null=True, blank=True
	)
	delivery_date_to_buyer = models.DateField(
		verbose_name='Дата поставки', null=True, blank=True
	)
	delivery_cost = models.PositiveIntegerField(
		verbose_name='Стоимость доставки', null=True, blank=True
	)
	calc_ready = models.BooleanField(
		editable=True, default=False, verbose_name='Просчет готов'
	)
	created = models.DateTimeField(
		auto_now_add=True, verbose_name='Создана'
	)
	edited = models.DateTimeField(
		auto_now=True, verbose_name='Изменена'
	)
	owner = models.ForeignKey(
		CustomUser, related_name='confirmed_calculate',
		verbose_name='Автор подтвержденного просчета',
		on_delete=models.SET_NULL, null=True
	)
	is_active = models.BooleanField(
		editable=True, default=True, verbose_name='is_active'
	)
	def __str__(self):
		return f'Просчет подтвержденный №{self.pk}'
