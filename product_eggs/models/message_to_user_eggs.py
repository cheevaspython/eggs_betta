from django.db import models

from general_layout.messages.models.message_to_user import MessageToUser
from product_eggs.models.calcs_deal_eggs import CalculateEggs, ConfirmedCalculateEggs, DealEggs
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs, LogicCardEggs


class MessageToUserEggs(MessageToUser):
	
	class Meta:
		db_table = 'MessageToUserEggs'
		verbose_name = 'Сообщение'
		verbose_name_plural = 'Сообщения'
		ordering = ['pk']
        
	current_deal = models.ForeignKey(
		DealEggs, related_name='Deal', on_delete=models.SET_NULL, null=True, blank=True
	)
	current_calculate = models.ForeignKey(
		CalculateEggs, related_name='Calculate', on_delete=models.SET_NULL, null=True, blank=True
	)
	current_conf_calculate = models.ForeignKey(
		ConfirmedCalculateEggs, related_name='ConfCalculate', 
		on_delete=models.SET_NULL, null=True, blank=True
	)
	current_seller = models.ForeignKey(
		SellerCardEggs, related_name='seller', on_delete=models.SET_NULL, null=True, blank=True
	)
	current_buyer = models.ForeignKey(
		BuyerCardEggs, related_name='buyer', on_delete=models.SET_NULL, null=True, blank=True
	)
	current_logic = models.ForeignKey(
		LogicCardEggs, related_name='logic', on_delete=models.SET_NULL, null=True, blank=True
	)
