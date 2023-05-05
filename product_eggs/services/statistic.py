from abc import ABC, abstractmethod

from product_eggs.models.base_client import LogicCardEggs, SellerCardEggs, BuyerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel


class BalanceClient(ABC):
    '''
    Интерфейс работы с балансом клиента.
    '''
    @abstractmethod
    def add_money_amount_for_buyer_form(self):
        '''
        Mетод оплаты покупателем.
        '''


class MultiPayOrderBalance(BalanceClient):
    '''
    Изменяет баланс клиента при общем платежном поручении.
    '''
    def __init__(self,
            pay_client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
            money_amount: float):

        self.pay_client = pay_client
        self.money_amount = money_amount

    def add_money_amount_for_buyer_form(self, cash: bool = False) -> None:

        if isinstance(self.pay_client, BuyerCardEggs):
            if cash:
                self.pay_client.balance_form_two += self.money_amount
                self.pay_client.save()
            else:
                self.pay_client.balance_form_one += self.money_amount
                self.pay_client.save()

    def __repr__(self) -> str:
        return f'{type(self).__name__}'


class BaseBalanceAbstract(BalanceClient):
    '''
    Базовый абстрактный класс по работе с балансом клиента.
    '''
    def __init__(self, current_model: BaseDealEggsModel,
            pay_client: SellerCardEggs | BuyerCardEggs | LogicCardEggs,
            money_amount: float): 
        self.current_deal = current_model
        self.money_amount = money_amount
        self.pay_client = pay_client

    def add_money_amount_for_buyer_form(self, UPD: bool = False):
        '''
        Mетод оплаты покупателем.
        '''

    def add_money_amount_to_logic(self, UPD: bool = False):
        '''
        Добавление в баланс логисту.
        '''

    def __repr__(self) -> str:
            return f'{type(self).__name__}'

        
class ContragentBalanceForm(BaseBalanceAbstract):
    '''
    Реализует метод оплаты покупателем, учитывает оплату по форме 2.
    '''
    def add_money_amount_for_buyer_form(self, UPD: bool = False) -> None:
        ...
        # if UPD:
        #     if isinstance(self.pay_client, BuyerCardEggs):
        #         if self.current_deal.cash:
        #             if self.current_deal.cash:
        #                 self.pay_client.balance_form_two -= self.money_amount
        #                 print(self.pay_client.balance_form_two)
        #                 self.pay_client.save()
        #                 print(self.pay_client.balance_form_two)
        #             else:
        #                 self.pay_client.balance_form_one -= self.money_amount
        #                 self.pay_client.save()
        # else:
        #     if isinstance(self.pay_client, BuyerCardEggs):
        #         if self.current_deal.cash:
        #             if self.current_deal.cash:
        #                 self.pay_client.balance_form_two += self.money_amount
        #                 self.pay_client.save()
        #             else:
        #                 self.pay_client.balance_form_one += self.money_amount
        #                 self.pay_client.save()

    def add_money_amount_to_logic(self, UPD: bool = False) -> None:
        '''
        Добавление в баланс логисту.
        '''
        # if UPD:
        #     if self.current_deal.delivery_form_payment == 3:
        #         self.pay_client.balance_form_two -= self.money_amount
        #         self.pay_client.save()
        #     else:
        #         self.pay_client.balance_form_one -= self.money_amount
        #         self.pay_client.save()
        # else:
        #     if self.current_deal.delivery_form_payment == 3:
        #         self.pay_client.balance_form_two += self.money_amount
        #         self.pay_client.save()
        #     else:
        #         self.pay_client.balance_form_one += self.money_amount
        #         self.pay_client.save()


