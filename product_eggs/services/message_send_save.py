from collections.abc import Iterable
from typing import Union

from django.db.models.query import QuerySet

from product_eggs.models.message_to_user_eggs import MessageToUserEggs
from product_eggs.models.calcs_deal_eggs import DealEggs, ConfirmedCalculateEggs, \
	CalculateEggs
from product_eggs.services.turn_off_fields import turn_off_fields_is_active
from users.models import CustomUser


def create_send_and_save_message(
		message_to_send:str, owner:CustomUser, /, deal=None, calculate=None,
		conf_calculate=None, seller=None, buyer=None, logic=None) -> None:
	"""
	Создает новую модель MessageToUserEggs.  
	"""
	message = MessageToUserEggs.objects.create(
		notification_to = owner,
		current_deal = deal,
		current_calculate = calculate,
		current_conf_calculate = conf_calculate,
		notification_message = message_to_send,
		current_seller = seller,
		current_buyer = buyer,
		current_logic = logic,
	)
	message.save()


def search_done_deal_messages_and_turn_off_fields_is_value(
		current_deal: DealEggs) -> None:     
	"""
	Ищет все сообщения для конкретной сделки,
	включая все вложенные сущности. Переводит их поле is_active в False.
	"""
	current_deal_messages = MessageToUserEggs.objects.filter(
		current_deal=current_deal).select_related(
    	'notification_to', 'current_conf_calculate', 'current_calculate', 'current_deal') 

	turn_off_fields_is_active(current_deal_messages)


def search_done_calc_and_conf_calc_messages_and_turn_off_fields_is_value(
		current_conf_calc: ConfirmedCalculateEggs) -> None:     
	"""
	Ищет все сообщения для конкретных моделях CalculateEggs, ConfirmedCalculateEggs,
	включая все вложенные сущности. Переводит их поле is_active в False.
	"""
	current_conf_calc_messages = MessageToUserEggs.objects.filter(
		current_conf_calculate=current_conf_calc).select_related(
    	'notification_to', 'current_conf_calculate', 'current_calculate', 'current_deal') 
	current_calc_messages = MessageToUserEggs.objects.filter(
		current_calculate=current_conf_calc.current_calculate).select_related(
    	'notification_to', 'current_conf_calculate', 'current_calculate', 'current_deal') 

	turn_off_fields_is_active(current_conf_calc_messages)
	turn_off_fields_is_active(current_calc_messages)


def send_message_to_users_queryset_deal_model(
		message: str, current_deal: DealEggs,
		queryset_customusers: Union[QuerySet[CustomUser], CustomUser]) -> None:
	"""
	Отправляет сообщение группе пользователей по модели DealEggs.
	"""
	try:
		if isinstance(queryset_customusers, Iterable):
			for customuser in queryset_customusers:
				create_send_and_save_message(message, customuser, deal=current_deal)
	except TypeError:
		if isinstance(queryset_customusers, CustomUser):
			create_send_and_save_message(message, queryset_customusers, deal=current_deal)     


def send_message_to_users_queryset_calculate_model(
		message: str, current_calculate: CalculateEggs,
		queryset_customusers: QuerySet[CustomUser]) -> None:
	"""
	Отправляет сообщение группе пользователей по модели CalculateEggs.
	"""
	try:
		for customuser in queryset_customusers:
			create_send_and_save_message(message, customuser, calculate=current_calculate)
	except TypeError:
			create_send_and_save_message(message, queryset_customusers[0], calculate=current_calculate)    


def send_message_to_users_queryset_conf_calculate_model(
		message: str, current_conf_calc: ConfirmedCalculateEggs,
		queryset_customusers: QuerySet[CustomUser]) -> None:
	"""
	Отправляет сообщение группе пользователей по модели ConfirmedCalculateEggs.
	"""
	try:
		for customuser in queryset_customusers:
			create_send_and_save_message(message, customuser, conf_calculate=current_conf_calc)
	except TypeError:
			create_send_and_save_message(message, queryset_customusers[0], conf_calculate=current_conf_calc)    

