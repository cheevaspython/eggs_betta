from abc import ABC, abstractmethod

from product_eggs.models.base_client import LogicCardEggs, SellerCardEggs, BuyerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.balance import get_cur_balance


class BalanceClient(ABC):
    '''
    Интерфейс работы с балансом клиента.
    '''
    @abstractmethod
    def add_money_amount_for_buyer_form(self):
        '''
        Mетод оплаты покупателем.
        '''


class BaseBalanceAbstract(BalanceClient):
    '''
    Базовый абстрактный класс по работе с балансом клиента.
    '''
    def __init__(self,
            current_model: BaseDealEggsModel,
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

    def add_money_amount_to_logic(self, UPD: bool = False) -> None:
        '''
        Добавление в баланс логисту.
        '''

