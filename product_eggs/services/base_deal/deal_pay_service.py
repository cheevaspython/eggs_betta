import logging
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist

from product_eggs.models.base_client import (
    BuyerCardEggs, LogicCardEggs, SellerCardEggs
)
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.base_deal.deal_pay_compare import (
    compare_UPD_and_payments, compare_payment_and_inital_amount
)
from product_eggs.services.data_class import PayOrderDataForSave

logger = logging.getLogger(__name__)


class DealPayOrderUPDservice():
    '''
    Класс для работы с пятью основными платежными документами.
    Исходящие УПД и ПП и входящие УПД и ПП. Входящая может быть общей.
    Добавляет или погашает долг по сделке, по которой приходит платежный документ.
    Отправляет сообщение финансовому директору при успешной операции,
    в случае выявления ошибок, raise exception оператору, который вводит данные.
    '''
    def __init__(self,
        data_detail: PayOrderDataForSave,
        current_deal: BaseDealEggsModel,
        pay_client: SellerCardEggs | BuyerCardEggs | LogicCardEggs):

        self.data = data_detail
        self.deal = current_deal
        self.pay_client = pay_client

    def try_to_create_payback_date_if_UPD_update(self) -> None:
        """
        Добавляет дату платежа по дате УПД.
        """
        DICT_UPD = {
            'UPD_incoming': self.add_payback_day_for_us,
            'UPD_outgoing': self.add_payback_day_for_buyer,
        }
        try:
            if self.data.doc_type in DICT_UPD:
                DICT_UPD[self.data.doc_type](self.data.date)
        except ObjectDoesNotExist:
            pass

    def add_payback_day_for_us(self, date_incoming_UPD: str) -> None:
        """
        Добавляет дату платежа по дате УПД для Пилигрим.
        """
        if self.deal.postponement_pay_for_us:
            convert_date_UPD = datetime.strptime(date_incoming_UPD, '%d/%m/%Y').date()
            payback_day = convert_date_UPD + timedelta(days=self.deal.postponement_pay_for_us)
            self.deal.payback_day_for_us = payback_day
        else:
            convert_date_UPD = datetime.strptime(date_incoming_UPD, '%d/%m/%Y').date()
            self.deal.payback_day_for_us = convert_date_UPD

    def add_payback_day_for_buyer(self, date_outgoing_UPD: str) -> None:
        """
        Добавляет дату платежа по дате УПД для Покупателя.
        """
        if self.deal.postponement_pay_for_buyer:
            convert_date_UPD = datetime.strptime(date_outgoing_UPD, '%d/%m/%Y').date()
            payback_day = convert_date_UPD + timedelta(days=self.deal.postponement_pay_for_us)
            self.deal.payback_day_for_buyer = payback_day
        else:
            convert_date_UPD = datetime.strptime(date_outgoing_UPD, '%d/%m/%Y').date()
            self.deal.payback_day_for_buyer = convert_date_UPD

    def add_or_replay_deal_debt(self):
        """
        Обрабатывает вводимые данные.
        """
        match self.data.doc_type:
            case 'UPD_incoming' | 'UPD_outgoing' | 'UPD_logic':
                if isinstance(self.pay_client, SellerCardEggs | BuyerCardEggs | LogicCardEggs):
                    self.deal = compare_UPD_and_payments(
                        self.deal,
                        self.pay_client,
                        self.data,
                    )

            case 'application_contract_logic':
                self.deal.delivery_cost = self.data.pay_quantity
                self.deal.logic_our_debt_for_app_contract = self.data.pay_quantity
                self.deal.logic_our_pay_amount -= self.data.pay_quantity

            case 'payment_order_outcoming_logic' | 'payment_order_outcoming' | 'payment_order_incoming' | 'tail_payment' | 'multi_pay_order':
                if isinstance(self.pay_client, SellerCardEggs | BuyerCardEggs | LogicCardEggs):
                    self.deal = compare_payment_and_inital_amount(
                        self.deal,
                        self.pay_client,
                        self.data,
                    )
            case _:
                logging.warning('field error in pay services, in type of tmp_json')
