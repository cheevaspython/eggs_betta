from typing import NamedTuple, Union

from django.db.models.query import QuerySet
from rest_framework import serializers

from product_eggs.models.calcs_deal_eggs import DealEggs
from product_eggs.services.message_send_save import create_send_and_save_message, \
	 send_message_to_users_queryset_deal_model, \
	 search_done_deal_messages_and_turn_off_fields_is_value
from product_eggs.services.turn_off_fields import turn_off_fields_is_active
from product_eggs.permissions.validate_user import super_users_and_buh_book
from users.models import CustomUser


class MessageAndOwnerToSendNotification(NamedTuple):
	message: str
	owner: Union[QuerySet[CustomUser], CustomUser]


def send_message_if_post_payment_to_seller(instance: DealEggs) -> None:
	message = f'Сделка №{instance.pk} на постоплате, проконтролируйте погрузку, \
		зафиксируйте фактическую дату погрузки и загрузите УПД'
	user = instance.seller_manager
	create_send_and_save_message(message, user, deal=instance)


def change_status_deal(current_deal:DealEggs, user: CustomUser) -> None:
	current_deal.status += 1
	current_deal.processing_to_confirm = True
	current_deal.save()
	check_processing_to_confirm(current_deal, user)


def check_user_permission_to_change_deal_status(obj:DealEggs, user: CustomUser) -> None:
	_, owner = get_message_and_user(obj)
	if user not in (owner,):
		if user not in super_users_and_buh_book():   
			raise serializers.ValidationError(f"You can't to confirm this deal №{obj.pk}")


def check_processing_to_confirm(current_deal:DealEggs, user: CustomUser) -> None:  
	if current_deal.processing_to_confirm:
		message_and_owner = get_message_and_user(current_deal)
		send_message_to_users_queryset_deal_model(message_and_owner.message, current_deal, message_and_owner.owner)
	else:
		check_user_permission_to_change_deal_status(current_deal, user)
		change_status_deal(current_deal, user)


def get_message_and_user(current_deal:DealEggs) -> MessageAndOwnerToSendNotification:
	match current_deal.status:
		case 1:		
			return MessageAndOwnerToSendNotification(
				f'Сделка №{current_deal.pk} ожидает подтверждения',
				CustomUser.objects.filter(role=6))
		case 2:
			return MessageAndOwnerToSendNotification(
				f'Основание для платежа, по сделке №{current_deal.pk}?',   
				current_deal.seller_manager)
		case 3:
			return MessageAndOwnerToSendNotification(
				f'Подтвердите оплату по сделке №{current_deal.pk}',
				CustomUser.objects.filter(role=6))
		case 4:
			return MessageAndOwnerToSendNotification(
				f'Оплатите закупку по сделке №{current_deal.pk} и загрузите подтверждение платежа',
				CustomUser.objects.filter(role=7))
		case 5:
			return MessageAndOwnerToSendNotification(
				f'Закупка по сделке №{current_deal.pk} оплачена, проконтролируйте погрузку, \
					зафиксируйте фактическую дату погрузки и загрузите УПД',   
				current_deal.seller_manager)
		case 6:
			return MessageAndOwnerToSendNotification(
				f'По сделке №{current_deal.pk} товар в пути, ожидаем от вас запрос исходящей УПД',
				current_deal.buyer_manager)
		case 7:
			return MessageAndOwnerToSendNotification(
				f'По сделке №{current_deal.pk} загрузите исходящую УПД',
				CustomUser.objects.filter(role=7))
		case 8:
			return MessageAndOwnerToSendNotification(
				f'Проконтролируйте разгрузку по сделке №{current_deal.pk}, \
					зафиксируйте фактическую дату разгрузки, загрузите подписанную УПД',
				current_deal.buyer_manager)
		case 9:  
			# add_debt_to_buyer(current_deal) 
			turn_off_fields_is_active(current_deal) #TODO
			search_done_deal_messages_and_turn_off_fields_is_value(current_deal)
			return MessageAndOwnerToSendNotification(
				f'Сделка №{current_deal.pk} закрыта',
				CustomUser.objects.filter(role=6),)
		case _: raise serializers.ValidationError(f'Deal №{current_deal.pk} completed')
