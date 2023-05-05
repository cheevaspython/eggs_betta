from django.db import models

from general_layout.messages.models.message_to_user import MessageToUser
from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
	ApplicationFromSellerBaseEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.base_client import BuyerCardEggs, \
	SellerCardEggs, LogicCardEggs


class MessageToUserEggs(MessageToUser):
	
	class Meta:
		db_table = 'MessageToUserEggs'
		verbose_name = 'Сообщение'
		verbose_name_plural = 'Сообщения'
		ordering = ['pk']
        
	current_base_deal = models.ForeignKey(
		BaseDealEggsModel, verbose_name='base_deal',
		on_delete=models.SET_NULL, null=True, blank=True
	)
	current_seller = models.ForeignKey(
		SellerCardEggs, verbose_name='seller',
		on_delete=models.SET_NULL, null=True, blank=True
	)
	current_buyer = models.ForeignKey(
		BuyerCardEggs, verbose_name='buyer',
		on_delete=models.SET_NULL, null=True, blank=True
	)
	current_logic = models.ForeignKey(
		LogicCardEggs, verbose_name='logic',
		on_delete=models.SET_NULL, null=True, blank=True
	)
	current_app_seller = models.ForeignKey(
		ApplicationFromBuyerBaseEggs, verbose_name='app_seller',
		on_delete=models.SET_NULL, null=True, blank=True
	)
	current_app_buyer = models.ForeignKey(
		ApplicationFromSellerBaseEggs, verbose_name='app_buyer',
		on_delete=models.SET_NULL, null=True, blank=True
	)




