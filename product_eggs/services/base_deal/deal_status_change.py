from rest_framework import serializers

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.permissions.validate_user import can_edit_deal
from product_eggs.services.data_class import BaseMessageForm, \
    MessageUserForDealStatus
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.messages.create_messages import MessagesCreator
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from product_eggs.services.messages.messages_services import \
    change_fileld_done_to_true, find_messages_where_base_deal_and_not_done, \
    search_done_base_deal_messages_and_turn_off
from users.models import CustomUser


class DealStatusChanger():
    """
    Check and change deal status.
    """
    def __init__(self, 
            instance: BaseDealEggsModel,
            user: CustomUser):

        if instance.status != 3:
            raise serializers.ValidationError(
                f'{self.instance} status !=3 !!!')
        self.instance = instance
        self.user = user

    def _check_status_conditions(self) -> str:
        """
        1. status_to_change 
        2. (if true) -> 
        3. (if status not 0 and 1 and < 9 )
        -> deal_status_owner_path (True)
        4. True + True -> check complete
        5. if == 9 -> 
        """
        if self.instance.deal_status_ready_to_change:
            if self.instance.deal_status <= 7:
                return 'change'
            elif self.instance.deal_status == 8:
                return 'complete'
            else:
                return 'pass'
        else:
            return 'pass'

    def status_changer_main(self):
        '''
        main start
        0. check user to can change 
        (superuser can change if check_status_conditions - False) 
        1. check_status_conditions
        2. send message
        3. change status
        '''
        match self._check_status_conditions():
            case 'pass':
                pass
            case 'change':
                if self.check_user_to_can_change():
                    self._change_deal_status()
                    self._send_action()
                else:
                    raise serializers.ValidationError(
                        'You cant change status this deal, or deal status is 8')
            case 'complete':
                self.instance.status += 1
                self.instance.deal_status += 1
                search_done_base_deal_messages_and_turn_off(self.instance) #TODO
                message = MessageLibrarrySend('deal_complete', self.instance)
                message.send_message()
                self.instance.save()
            case _: pass

    def _send_action(self):
        """
        send message to current user for change status
        to next position
        """
        message_user = self._get_message_and_user()
        action = MessagesCreator(
            BaseMessageForm(
                message_user.message,
                self.instance,
                message_user.owner)
        )
        action.create_message()

    def _change_deal_status(self):
        """
        change status, reset user patch bool,
        set action to process, save
        """
        self.instance.deal_status += 1
        self.instance.deal_status_ready_to_change = False
        self.instance.save()
        change_fileld_done_to_true(
            find_messages_where_base_deal_and_not_done(self.instance.pk))

    def check_user_to_can_change(self) -> bool:
        """
        Compare entry user and action user | users.role 
        in deal status library
        """
        #check status
        if self.instance.deal_status > 8:
            return False
        #check superuser
        if self.user in can_edit_deal():
            return True
        message_user = self._get_message_and_user()

        try:
            if isinstance(message_user.owner, CustomUser):
                return True if self.user == message_user.owner else False
            return True if self.user.role == message_user.owner[-1].role else False
        except IndexError as e:
            raise serializers.ValidationError(f'you havent some users role! {e}')
    
    @try_decorator_param(('AttributeError',))
    def _get_message_and_user(self) -> MessageUserForDealStatus:
        """
        return action and current user | users for condition
        """
        _messages_and_users_library = {
            1: MessageUserForDealStatus(
				f'Сделка №{self.instance.documents.pk} \
				    ожидает подтверждения',
				CustomUser.objects.filter(role=6)
                ),
            2: MessageUserForDealStatus(
				f'Основание для платежа, по сделке \
				    №{self.instance.documents.pk}.',   
				self.instance.seller.manager
				),
            3: MessageUserForDealStatus(
				f'Подтвердите оплату по сделке \
				    №{self.instance.documents.pk}',
				CustomUser.objects.filter(role=6)
                ),
            4: MessageUserForDealStatus(
				f'Оплатите закупку по сделке \
				    №{self.instance.documents.pk} и \
				    загрузите подтверждение платежа',
				CustomUser.objects.filter(role=7)
				),
			5: MessageUserForDealStatus(
				f'Закупка по сделке №{self.instance.documents.pk} \
				    оплачена, проконтролируйте погрузку, зафиксируйте \
				    фактическую дату погрузки и загрузите УПД',   
				self.instance.seller.manager
				),
            6: MessageUserForDealStatus(
				f'По сделке №{self.instance.documents.pk} товар \
				    в пути, ожидаем от вас запрос исходящей УПД',
				self.instance.buyer.manager
				),
			7: MessageUserForDealStatus(
				f'По сделке №{self.instance.documents.pk} \
				    загрузите исходящую УПД',
				CustomUser.objects.filter(role=7)
				),
			8: MessageUserForDealStatus(
				f'Проконтролируйте разгрузку по сделке \
				    №{self.instance.documents.pk}, зафиксируйте \
				    фактическую дату разгрузки, загрузите подписанную УПД',
				self.instance.buyer.manager
				),
        }
        return _messages_and_users_library[self.instance.deal_status]
