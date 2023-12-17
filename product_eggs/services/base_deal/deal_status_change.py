from datetime import datetime
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.permissions.validate_user import can_edit_deal_super_user
from product_eggs.services.data_class import (
    BaseMessageForm, MessageUserForDealStatus
)
from product_eggs.services.decorators import try_decorator_param
from product_eggs.services.messages.create_messages import MessagesCreator
from product_eggs.services.messages.messages_library import MessageLibrarrySend
from product_eggs.services.messages.messages_services import (
    change_fileld_done_to_true, find_messages_where_base_deal_and_not_done,
    search_done_base_deal_messages_and_turn_off
)
from product_eggs.services.validationerror import custom_error
from users.models import CustomUser


class DealStatusChanger():
    """
    Check and change deal status.
    """
    def __init__(
            self,
            instance: BaseDealEggsModel,
            user: CustomUser,
            close: str = '',
        ):
        if instance.status != 3:
            raise custom_error(f'bas_deal_model status !=3 !!!', 433)

        self.instance = instance
        self.user = user
        self.close = close

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
            if self.instance.deal_status == 0:
                return 'new_deal'
            elif self.instance.deal_status <= 9 and self.instance.deal_status_multi:
                return 'half_action'
            elif self.instance.deal_status <= 9:
                return 'change'
            elif self.instance.deal_status == 10 and self.close:
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
            case 'new_deal':
                self._change_deal_status()
                self._send_action()
            case 'half_action':
                if self.check_user_to_can_change():
                    self.instance.deal_status_multi = False
                    self.instance.deal_status_ready_to_change = False
                    self.instance.save()
                else:
                    raise custom_error(
                        'You cant change status this deal, or deal status is 9 or im stupid coder', 433)
            case 'change':
                if self.check_user_to_can_change():
                    self._change_deal_status()
                    self._send_action()
                else:
                    raise custom_error(
                        'You cant change status this deal, or deal status is 9', 433)
            case 'complete':
                self.instance.status += 1
                self.instance.deal_status += 1
                self.instance.close_deal_date = datetime.strptime(self.close, "%d/%m/%Y")
                search_done_base_deal_messages_and_turn_off(self.instance) #TODO
                self.instance.save()
                self.send_message_deal_complete()
                self.change_applications_actual_and_send_message()
            case 'pass':
                pass
            case _:
                pass

    def send_message_deal_complete(self):
        """
        send deal complete message to finance manager and applications managers if different
        """
        message_fin = MessageLibrarrySend('deal_complete', self.instance)
        message_fin.send_message()
        message_seller_manager = MessageLibrarrySend(
            'deal_complete', self.instance, user_from=self.instance.application_from_seller.owner,
        )
        message_seller_manager.send_message()
        if self.instance.application_from_buyer.owner != self.instance.application_from_seller.owner:
            message_buyer_manager = MessageLibrarrySend(
                'deal_complete', self.instance, user_from=self.instance.application_from_buyer.owner,
            )
            message_buyer_manager.send_message()

    def change_applications_actual_and_send_message(self):
        """
        change action in applications -> to False, send message managers
        """
        self.instance.application_from_buyer.is_actual = False
        self.instance.application_from_seller.is_actual = False
        self.instance.application_from_buyer.save()
        self.instance.application_from_seller.save()
        owner_buyer_message = MessageLibrarrySend(
            'applications_actual',
            self.instance.application_from_buyer,
            user_from=self.instance.application_from_buyer.owner,
        )
        owner_seller_message = MessageLibrarrySend(
            'applications_actual',
            self.instance.application_from_seller,
            user_from=self.instance.application_from_seller.owner,
        )
        owner_buyer_message.send_message()
        owner_seller_message.send_message()

    def _send_action(self):
        """
        send message to current user for change status
        to next position
        """
        message_user = self._get_message_and_user()
        if isinstance(message_user, tuple) and self.instance.documents.edo_seller_documents:
            self.instance.deal_status_multi = True
            for cur_action in message_user:
                action = MessagesCreator(
                    BaseMessageForm(
                        cur_action.message,
                        self.instance,
                        cur_action.owner)
                )
                action.create_message()
                self.instance.save()
        elif isinstance(message_user, MessageUserForDealStatus):
            action = MessagesCreator(
                BaseMessageForm(
                    message_user.message,
                    self.instance,
                    message_user.owner)
            )
            action.create_message()
        else:
            raise custom_error('wrong return data in _send_action deal changer', 433)

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

    def check_user_to_can_change(self) -> bool | None:
        """
        Compare entry user and action user | users.role
        in deal status library
        """
        #check status
        if self.instance.deal_status > 9:
            return False
        #check superuser
        if self.user in can_edit_deal_super_user():
            return True

        message_user = self._get_message_and_user()
        if isinstance(message_user, tuple):
            try:
                for cur_message_user in message_user:
                    if isinstance(cur_message_user.owner, CustomUser):
                        if self.user == cur_message_user.owner:
                            return True
                    else:
                        if self.user in cur_message_user.owner:
                            return True
                return False
            except IndexError as e:
                raise custom_error(f'you havent some users role! {e}', 433)

        elif isinstance(message_user, MessageUserForDealStatus):
            try:
                if isinstance(message_user.owner, CustomUser):
                    return True if self.user == message_user.owner else False
                else:
                    return True if self.user in message_user.owner else False
            except IndexError as e:
                raise custom_error(f'you havent some users role! {e}', 433)

    @try_decorator_param(('AttributeError',))
    def _get_message_and_user(self) -> MessageUserForDealStatus | tuple[MessageUserForDealStatus]:
        """
        return action and current user | users for condition
        """
        if self.instance.seller.manager and self.instance.buyer.manager:
            try:
                _messages_and_users_library = {
                    1: MessageUserForDealStatus(
                        f'Сделка №{self.instance.pk} ожидает подтверждения',
                        CustomUser.objects.filter(role=6),
                    ),
                    2: MessageUserForDealStatus(
                        f'Основание для платежа, по сделке №{self.instance.pk}.',
                        self.instance.application_from_seller.owner,
                    ),
                    3: MessageUserForDealStatus(
                        f'Подтвердите оплату по сделке №{self.instance.pk}',
                        CustomUser.objects.filter(role=6),
                    ),
                    4: MessageUserForDealStatus(
                        f'Оплатите закупку по сделке №{self.instance.pk} и \
                        загрузите подтверждение платежа',
                        CustomUser.objects.filter(role=7),
                    ),
                    5: MessageUserForDealStatus(
                        f'Закупка по сделке №{self.instance.pk} \
                        оплачена, проконтролируйте погрузку и загрузите УПД',
                        self.instance.application_from_seller.owner,
                    ),
                    6: MessageUserForDealStatus(
                        f'По сделке №{self.instance.pk} товар \
                        в пути, ожидаем от вас запрос исходящей УПД',
                        self.instance.application_from_buyer.owner,
                    ),
                    7: MessageUserForDealStatus(
                        f'По сделке №{self.instance.pk} загрузите исходящую УПД',
                        CustomUser.objects.filter(role=7),
                    ),
                    8: MessageUserForDealStatus(
                        f'Проконтролируйте разгрузку по сделке \
                        №{self.instance.pk} и загрузите подписанную УПД',
                        self.instance.application_from_buyer.owner,
                    ),
                    9: MessageUserForDealStatus( #TODO double messaage, add to logic?
                        f'По сделке №{self.instance.pk} произведена разгрузка и  \
                        загружена исходящяя подписанная УПД, загрузите пп для перевозчика, \
                        проверьте наличие всех необходимых для бухгалтерии сканов \
                        документов',
                        CustomUser.objects.filter(role=7),
                    ),
                }
                _messages_and_users_library_edo = {
                    1: MessageUserForDealStatus(
                        f'Сделка №{self.instance.pk} ожидает подтверждения',
                        CustomUser.objects.filter(role=6),
                    ),
                    2: MessageUserForDealStatus(
                        f'Основание для платежа, по сделке №{self.instance.pk}.',
                        self.instance.application_from_seller.owner,
                    ),
                    3: MessageUserForDealStatus(
                        f'Подтвердите оплату по сделке №{self.instance.pk}',
                        CustomUser.objects.filter(role=6),
                    ),
                    4: MessageUserForDealStatus(
                        f'Оплатите закупку по сделке №{self.instance.pk} и \
                        загрузите подтверждение платежа',
                        CustomUser.objects.filter(role=7),
                    ),
                    5: (
                        MessageUserForDealStatus(
                            f'Закупка по сделке №{self.instance.pk} \
                            оплачена, проконтролируйте погрузку',
                            self.instance.application_from_seller.owner,
                        ),
                        MessageUserForDealStatus(
                            f'По сделке №{self.instance.pk} \
                            загрузите в систему данные по входящей УПД (ЭДО)',
                            CustomUser.objects.filter(role=7),
                        ),
                    ),
                    6: MessageUserForDealStatus(
                        f'По сделке №{self.instance.pk} товар \
                        в пути, ожидаем от вас запрос исходящей УПД',
                        self.instance.application_from_buyer.owner,
                    ),
                    7: MessageUserForDealStatus(
                        f'По сделке №{self.instance.pk}, \
                        загрузите в систему данные по входящей УПД (ЭДО), \
                        а также загрузите исходящую УПД',
                        CustomUser.objects.filter(role=7),
                    ),
                    8: MessageUserForDealStatus(
                        f'Проконтролируйте разгрузку по сделке №{self.instance.pk}.',
                        self.instance.application_from_buyer.owner,
                    ),
                    9: MessageUserForDealStatus(
                        f'По сделке №{self.instance.pk}, разгрузка произведена, \
                        загрузите в систему данные по исходящей УПД (ЭДО), \
                        загрузите пп для перевозчика, \
                        проверьте наличие всех необходимых для бухгалтерии сканов \
                        документов',
                        CustomUser.objects.filter(role=7),
                    ),
                }
                result = _messages_and_users_library[self.instance.deal_status]
                if self.instance.documents.edo_seller_documents or self.instance.documents.edo_buyer_documents:
                    result = _messages_and_users_library_edo[self.instance.deal_status]
                return result

            except Exception as e:
                raise custom_error(f'status = {self.instance.deal_status}, something wrong, error -> {e}', 433)
        else:
            raise custom_error(f'deal -> {self.instance.pk} errror in message model seller/buyer manager == None!', 433)
