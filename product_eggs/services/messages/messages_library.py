from typing import Union

from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.services.data_class import BaseMessageForm
from product_eggs.services.messages.create_messages import MessagesCreator
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs, \
    LogicCardEggs
from product_eggs.services.validationerror import custom_error
from users.models import CustomUser


class MessageLibrarrySend():
    """
    Messages book.
    """
    action_client_book = ()
    action_applications_book = (
        'applications_actual',
        'applications_await_cost',
        'comment to app_buyer',
        'comment to app_seller',
    )
    action_logic_book = (
        'message_50_50_payment',
        'message_100_payment',
        'message_advance_payment',
    )
    action_general_book = (
        'message_to_finance_director',
    )
    action_base_model_book = (
        'comment to base_deal',
        'confirm_new_calc',
        'calc_confirmed',
        'conf_calc_wait_logic',
        'note_calc',
        'note_conf_calc',
        'logic_confirmed',
        'logic_confirmed_delivery_by_seller',
        'calc_ready',
        'conf_calc_confirmed_deal_create',
    )
    action_base_model_deal_book = (
        'deal_complete',
        'if_post_payment_to_seller'
    )

    def __init__(self,
            action: str,
            model: Union[
                BuyerCardEggs, SellerCardEggs,
                LogicCardEggs, BaseDealEggsModel,
                ApplicationFromBuyerBaseEggs,
                ApplicationFromSellerBaseEggs,
            ],
            message: str | None = None,
            user_from: CustomUser | None = None,
            ):

        self.action = action
        self.model = model
        self.message = message
        self.user = user_from

    def send_message(self):
        """
        Compare action and action book.

        """
        if self.action in self.action_client_book:
            self.send_client_book()
        elif self.action in self.action_base_model_book:
            self.send_base_model_book()
        elif self.action in self.action_logic_book:
            self.send_logic_book()
        elif self.action in self.action_base_model_deal_book:
            self.send_base_model_deal_book()
        elif self.action in self.action_general_book:
            self.send_general_book()
        elif self.action in self.action_applications_book:
            self.send_applications_book()

    def send_general_book(self):
        """
        Send message general book.
        """
        if self.message and isinstance(self.model, BaseDealEggsModel):
            client_library = {
                'message_to_finance_director': BaseMessageForm(
                    self.message,
                    self.model,
                    CustomUser.objects.filter(role=6),
                    info=True,
                ),
            }
            message = MessagesCreator(client_library[self.action])
            message.create_message()

    def send_client_book(self):
        """
        Send message BuyerCardEggs, SellerCardEggs.
        """

    def send_applications_book(self):
        """
        Send message BuyerCardEggs, SellerCardEggs.
        """
        if isinstance(self.model,
                ApplicationFromSellerBaseEggs | ApplicationFromBuyerBaseEggs) and self.model.owner:
            if self.user:
                cur_user = self.user
            else:
                cur_user = self.model.owner
            applications_library = {
                'applications_actual': BaseMessageForm(
                    f'Проверьте актуальность заявки №{self.model.pk}.',
                    self.model,
                    cur_user,
                    info=True,
                ),
                'applications_await_cost': BaseMessageForm(
                    f'Заполните данные договорной заявки №{self.model.pk}.',
                    self.model,
                    cur_user,
                    info=True,
                ),
            }
            applications_library_message = {
                'comment to app_seller': BaseMessageForm(
                    f'Добавлен комментарий для заявки от продавца №{self.model.pk}: {self.message}.',
                    self.model,
                    cur_user,
                    info=True,
                ),
                'comment to app_buyer': BaseMessageForm(
                    f'Добавлен комментарий для заявки от покупателя №{self.model.pk}: {self.message}.',
                    self.model,
                    cur_user,
                    info=True,
                ),
            }
            if self.message:
                message = MessagesCreator(applications_library_message[self.action])
                message.create_message()
            else:
                message = MessagesCreator(applications_library[self.action])
                message.create_message()

    def send_logic_book(self):
        """
        Send message LogicCardEggs.
        """
        if isinstance(self.model, BaseDealEggsModel):
            logic_library = {
                'message_50_50_payment': BaseMessageForm(
                    (f'По сделке №{self.model.pk} загружен скан акт-упд перевозчика' +
                    f'Проверьте и оплатите 50%'),
                    self.model,
                    CustomUser.objects.filter(role=7)
                ),
                'message_100_payment': BaseMessageForm(
                    (f'По сделке №{self.model.pk} загружен скан акт-упд перевозчика' +
                    f'Проверьте и оплатите 100%'),
                    self.model,
                    CustomUser.objects.filter(role=7)
                ),
            }
            logic_message_library = {
                'message_advance_payment': BaseMessageForm(
                    f'По сделке №{self.model.pk} оплатите аванс в размере {self.message}',
                    self.model,
                    CustomUser.objects.filter(role=7)
                ),
            }
            if self.message:
                message = MessagesCreator(logic_message_library[self.action])
                message.create_message()
            else:
                message = MessagesCreator(logic_library[self.action])
                message.create_message()

    def send_base_model_deal_book(self):
        if self.user:
            cur_user = self.user
        else:
            cur_user = CustomUser.objects.filter(role=6)
        if isinstance(self.model, BaseDealEggsModel):
            if self.model.documents and self.model.seller.manager:
                base_model_library_status_deal = {
                    'deal_complete': BaseMessageForm(
                        f'Сделка №{self.model.pk} закрыта',
                        self.model,
                        cur_user,
                        info=True,
                    ),
                    'if_post_payment_to_seller': BaseMessageForm(
                        f'Сделка №{self.model.pk} на постоплате, \
                        проконтролируйте погрузку, зафиксируйте фактическую \
                        дату погрузки и загрузите УПД',
                        self.model,
                        self.model.seller.manager,
                    ),
                }
                message = MessagesCreator(base_model_library_status_deal[self.action])
                message.create_message()
            else:
                raise custom_error(
                    f'deal model: {self.model}, havent relation with deal_docs!', 433)

    def send_base_model_book(self):
        if isinstance(self.model, BaseDealEggsModel) and self.model.owner:
            base_model_library = {
                'confirm_new_calc': BaseMessageForm(
                    f'Просчет №{self.model.pk} готов к подтверждению.',
                    self.model,
                    CustomUser.objects.filter(role=5),
                ),
                'calc_confirmed': BaseMessageForm(
                    f'Просчет №{self.model.pk} подтвержден',
                    self.model,
                    self.model.owner,
                    info=True,
                ),
                'conf_calc_wait_logic': BaseMessageForm(
                    f'Подтвержденный просчет №{self.model.pk} создан \
                        и ожидает добавления перевозчика',
                    self.model,
                    CustomUser.objects.filter(role=4),
                ),
                'logic_confirmed': BaseMessageForm(
                    f'Перевозчик добавлен в подтвержденный просчет №{self.model.pk}, \
                        готов к отправке на подтверждение менеджеру направления',
                    self.model,
                    self.model.owner,
                ),
                'logic_confirmed_delivery_by_seller': BaseMessageForm(
                    f'В просчете №{self.model.pk} перевозку осуществляет продавец, \
                        сверьте остальные данные и отправляйте на подтверждение менеджеру направления',
                    self.model,
                    self.model.owner,
                ),
                'calc_ready': BaseMessageForm(
                    f'Одобрите подтвержденный просчет №{self.model.pk} \
                        для перехода в статус Сделка.',
                    self.model,
                    CustomUser.objects.filter(role=5)
                ),
                'conf_calc_confirmed_deal_create': BaseMessageForm(
                    f'Подтвержденный просчет №{self.model.pk} одобрен, сделка создана.',
                    self.model,
                    self.model.owner,
                    info=True,
                ),
            }
            base_model_library_message = {
                'note_calc': BaseMessageForm(
                    f'Замечание по просчету №{self.model.pk} {self.message}',
                    self.model,
                    self.model.owner,
                ),
                'note_conf_calc': BaseMessageForm(
                    f'Замечание по подтвержденному просчету №{self.model.pk} {self.message}',
                    self.model,
                    self.model.owner,
                ),
                'comment to base_deal': BaseMessageForm(
                    f'Добавлен комментарий для {self.model}: {self.message}.',
                    self.model,
                    self.model.owner,
                    info=True,
                ),
            }
            if self.message:
                message = MessagesCreator(base_model_library_message[self.action])
                message.create_message()
            else:
                message = MessagesCreator(base_model_library[self.action])
                message.create_message()

