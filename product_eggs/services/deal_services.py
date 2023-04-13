from datetime import datetime, timedelta
from collections import OrderedDict

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from product_eggs.models.calcs_deal_eggs import DealEggs
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs
from product_eggs.services.create_expense_model import documents_model_creator, origins_model_creator
from product_eggs.services.messages_library import send_message_to_finance_director 
from product_eggs.services.statistic import BaseBalanceAbstract
from product_eggs.serializers.additional_expense_serializer import AdditionalExpenseEggsDetailSerializer
from product_eggs.services.data_class import PayOrderDataForSave


class DealPayOrderUPDservice():
    '''
    Класс для работы с пятью основными платежными документами. 
    Исходящие УПД и ПП и входящие УПД и ПП. Входящая может быть общей.
    Добавляет или погашает долг по сделке, по которой приходит платежный документ. 
    Отправляет сообщение финансовому директору при успешной операции,
    в случае выявления ошибок, raise exception оператору, который вводит данные.
    '''
    def __init__(self, 
        dict_data_detail: PayOrderDataForSave,
        current_deal: DealEggs,
        pay_client: SellerCardEggs | BuyerCardEggs,
        balance: BaseBalanceAbstract):
        
        self.data = dict_data_detail
        self.deal = current_deal
        self.pay_client = pay_client 
        self._balance = balance

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
        except ObjectDoesNotExist as e:
            print(e)

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
            case 'UPD_incoming':
                if self.deal.current_deal_our_debt:
                    raise serializers.ValidationError(
                        f"По сделке №{self.deal.pk} долг перед нами уже зафиксирован, " +
                        f"проверьте данные"
                        )
                else:
                    self.deal.current_deal_our_debt += self.data.pay_quantity
                    self.deal.deal_our_debt_UPD += self.data.pay_quantity
                    self._balance.add_money_amount_for_buyer_form(UPD=True)
            case 'UPD_outgoing':
                if self.deal.current_deal_buyer_debt:
                    raise serializers.ValidationError(
                        f"По сделке №{self.deal.pk} долг перед продавцом уже зафиксирован, " +
                        f"проверьте данные"
                        )
                else:
                    self.deal.current_deal_buyer_debt += self.data.pay_quantity
                    self.deal.deal_buyer_debt_UPD += self.data.pay_quantity
                    self._balance.add_money_amount_for_buyer_form(UPD=True)
            case 'payment_order_outcoming':
                if self.deal.current_deal_our_debt <= 0: 
                    raise serializers.ValidationError(
                        f'У сделки №{self.deal.pk}, долга перед продавцом нет, проверьте данные'
                        )
                else:
                    old_debt = self.deal.current_deal_our_debt 
                    self.deal.current_deal_our_debt -= self.data.pay_quantity
                    if self.deal.current_deal_our_debt < 0:
                        raise serializers.ValidationError(
                            f"У сделки №{self.deal.pk}, наш долг перед продавцом составляет - {old_debt}, " +
                            f"Вы вностите {self.data.pay_quantity}, разница составляет -" +
                            f"{self.deal.current_deal_our_debt}, проверьте данные"
                            )
                    elif self.deal.current_deal_our_debt == 0:
                        self._balance.add_money_amount_for_buyer_form()
                        send_message_to_finance_director(
                            f"По сделке №{self.deal.pk} - долг перед продавцом закрыт" + 
                            f"ПП от {self.pay_client}/{self.data.inn} на сумму {self.data.pay_quantity}",
                            self.pay_client,
                            )
                    else:
                        self._balance.add_money_amount_for_buyer_form()
                        send_message_to_finance_director(
                            f"ПП от {self.pay_client}/{self.data.inn} по сделке №{self.deal.pk}, " +
                            f"на сумму {self.data.pay_quantity} внесен, " +
                            f"остаток долга перед продавцом составляет - " +
                            f"{self.deal.current_deal_our_debt}",
                            self.pay_client,
                            )
            case 'payment_order_incoming':
                if self.deal.current_deal_buyer_debt <= 0: 
                    raise serializers.ValidationError(
                        f'У сделки №{self.deal.pk} долга перед нами нет, проверьте данные'
                        )
                else:
                    old_debt = self.deal.current_deal_buyer_debt 
                    self.deal.current_deal_buyer_debt -= self.data.pay_quantity
                    if self.deal.current_deal_buyer_debt < 0:
                        raise serializers.ValidationError(
                            f"У сделки №{self.deal.pk}, долг перед нами составляет - {old_debt}, " +
                            f"Вы вностите {self.data.pay_quantity}, разница составляет -" +
                            f"{self.deal.current_deal_buyer_debt}, проверьте данные"
                            )
                    elif self.deal.current_deal_buyer_debt == 0:
                        self._balance.add_money_amount_for_buyer_form()
                        send_message_to_finance_director(
                            f"По сделке №{self.deal.pk} - долг перед нами закрыт" + 
                            f"ПП от {self.pay_client}/{self.data.inn} на сумму {self.data.pay_quantity}",
                            self.pay_client,
                            )
                    else:
                        self._balance.add_money_amount_for_buyer_form()
                        send_message_to_finance_director(
                            f"ПП от {self.pay_client}/{self.data.inn} по сделке №{self.deal.pk}, " +
                            f"на сумму {self.data.pay_quantity} внесен, " +
                            f"остаток долга перед нами составляет - " +
                            f"{self.deal.current_deal_buyer_debt}",
                            self.pay_client,
                            )
            case _:
                print('field_error in DealPayOrderUPDservice')


def create_relation_deal_orig_and_docs_if_not_None(instance: DealEggs) -> None:
    """
    Создает внешний ключ на модель документов по сделке.
    """
    if instance.documents is None:   
        instance.documents = documents_model_creator()
        instance.documents.origins = origins_model_creator()
        instance.documents.save()
        instance.save()
    else:
        return print('docs_relation not None')


def get_additional_exp_detail(instance: DealEggs) -> OrderedDict:
    """
    Возвращает детали дополнительного расхода по сделке.
    """
    model = AdditionalExpenseEggs.objects.get(id=instance.additional_expense)
    return_data = AdditionalExpenseEggsDetailSerializer(model)
    return return_data.data


def try_to_get_deal_model(deal_id: int) -> DealEggs | None:
    """
    Получает модель сделки по pk.
    """
    try:
        return DealEggs.objects.get(pk=deal_id) 
    except:
        raise serializers.ValidationError('invalid deal_id')


def try_to_get_deal_model_for_doc_deal_id(doc_deal_id: int) -> DealEggs | None:
    """
    Получает модель сделки по pk документов к сделке.
    """
    try:
        return DealEggs.objects.get(pk=doc_deal_id) 
    except:
        raise serializers.ValidationError('invalid deal_id')


def try_to_get_deal_docs_model(docs_id: int) -> DocumentsDealEggsModel | None:
    """
    Получает модель документов к сделке по pk.
    """
    try:
        return DocumentsDealEggsModel.objects.get(pk=docs_id) 
    except:
        raise serializers.ValidationError('invalid document_id or relation for deal')


