from typing import Union

from rest_framework import serializers

from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.services.data_class import BaseMessageForm
from product_eggs.services.messages.create_messages import MessagesCreator
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs, \
    LogicCardEggs
from users.models import CustomUser


class MessageLibrarrySend():
    """
    Messages book.  
    """
    action_client_book = ()
    action_applications_book = (
        'applications_actual',
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
        'create_new_calc',
        'calc_confirmed',
        'conf_calc_wait_logic',
        'note_calc',
        'note_conf_calc',
        'logic_confirmed',
        'calc_ready',
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
            message: str | None = None,):

        self.action = action
        self.model = model
        self.message = message

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
                ApplicationFromSellerBaseEggs | ApplicationFromBuyerBaseEggs):
            applications_library_message = {
                'applications_actual': BaseMessageForm(
                    f'Проверьте актуальность заявки №{self.model.pk}.',
                    self.model,
                    self.model.owner,
                    ),
            }
            if self.message:
                pass
            else:
                message = MessagesCreator(applications_library_message[self.action])
                message.create_message()

    def send_logic_book(self):
        """
        Send message LogicCardEggs.
        """
        if isinstance(self.model, BaseDealEggsModel):
            logic_library = {
                'message_50_50_payment': BaseMessageForm(
                    (f'По сделке №{self.model.documents.pk} загружен скан акт-упд перевозчика' +
                    f'Проверьте и оплатите 50%'),
                    self.model,
                    CustomUser.objects.filter(role=7)
                    ),
                'message_100_payment': BaseMessageForm(
                    (f'По сделке №{self.model.documents.pk} загружен скан акт-упд перевозчика' +
                    f'Проверьте и оплатите 100%'),
                    self.model,
                    CustomUser.objects.filter(role=7)
                    ),
            }
            logic_message_library = {
                'message_advance_payment': BaseMessageForm(
                    f'По сделке №{self.model.documents.pk} оплатите аванс в размере {self.message}',
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
        if isinstance(self.model, BaseDealEggsModel):
            if self.model.documents:
                base_model_library_status_deal = {
                    'deal_complete': BaseMessageForm(
                        f'Сделка №{self.model.documents.pk} закрыта',
                        self.model,
                        CustomUser.objects.filter(role=6),
                        ),
                    'if_post_payment_to_seller': BaseMessageForm(
                        f'Сделка №{self.model.documents.pk} на постоплате, \
                        проконтролируйте погрузку, зафиксируйте фактическую \
                        дату погрузки и загрузите УПД',
                        self.model,
                        self.model.seller.manager,
                        ),
                }
                message = MessagesCreator(base_model_library_status_deal[self.action])
                message.create_message()
            else:
                raise serializers.ValidationError(
                    f'deal model: {self.model}, havent relation with deal_docs!')

    def send_base_model_book(self):
        if isinstance(self.model, BaseDealEggsModel):
            base_model_library = {
                'create_new_calc': BaseMessageForm(
                    f'Создан новый просчет №{self.model.pk}',
                    self.model,
                    CustomUser.objects.filter(role=5)
                    ),
                'calc_confirmed': BaseMessageForm(
                    f'Просчет №{self.model.pk} подтвержден',
                    self.model,
                    self.model.owner,
                    ),
                'conf_calc_wait_logic': BaseMessageForm(
                    f'Подтвержденный просчет №{self.model.pk} создан \
                        и ожидает добавления перевозчика',
                    self.model,
                    CustomUser.objects.filter(role=4)
                    ),
                'logic_confirmed': BaseMessageForm(
                    f'Логист добавлен в подтвержденный просчет №{self.model.pk}, \
                        готов к отправке на подтверждение менеджеру направления',
                    self.model,
                    self.model.owner,
                    ),
                'calc_ready': BaseMessageForm(
                    f'Одобрите подтвержденный просчет №{self.model.pk} \
                        для перехода в статус Сделка.',
                    self.model,
                    CustomUser.objects.filter(role=5)
                    ),
            }
            base_model_library_message = {
                'note_calc': BaseMessageForm(
                    f'Замечание по просчету №{self.model.pk}: \
                    \n {self.message}',
                    self.model,
                    self.model.owner,
                    ),
                'note_conf_calc': BaseMessageForm(
                    f'Замечание по подтвержденному просчету \
                    №{self.model.pk}: \
                    \n {self.message}',
                    self.model,
                    self.model.owner,
                    ),
            }
            if self.message:
                message = MessagesCreator(base_model_library_message[self.action])
                message.create_message()
            else:
                message = MessagesCreator(base_model_library[self.action])
                message.create_message()

