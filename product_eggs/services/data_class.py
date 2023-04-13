from dataclasses import dataclass
from typing import Optional, Union
from datetime import datetime
from django.db.models import QuerySet

from rest_framework_simplejwt.views import serializers
from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel

from users.models import CustomUser


@dataclass
class PayOrderDataForSave():
    """
    Dataclass для упорядочивания данных,
    по финансовым документам, для сохранения в базу.
    """
    user: CustomUser
    date: datetime
    number: str
    pay_quantity: float | str
    inn: str
    deal: str
    doc_type: str
    documents_id: str 

    def __post_init__(self):
        self.pay_quantity = float(self.pay_quantity)

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass()
class OtherPays():
    """
    Dataclass для упорядочивания данных,
    для общего платежного поручения, 
    для поля со сделками.
    """
    deal: str
    documents_id: str
    pay_quantity: str | float
    doc_type: str = ''

    def __post_init__(self):
        self.doc_type = 'payment_order_incoming'
        self.pay_quantity = float(self.pay_quantity)

    def __getitem__(self, item):
        return getattr(self, item)
 

@dataclass
class PayOrderDataForSaveMulti():
    """
    Dataclass для упорядочивания данных,
    для общего платежного поручения. 
    """
    user: CustomUser
    date: datetime
    number: str
    inn: str
    total_amount: str | float
    tail_form_one: str | float | None
    tail_form_two: str | float | None
    other_pays: list | Optional[OtherPays]

    def __post_init__(self):
        try:
            self.total_amount = float(self.total_amount)
            if self.tail_form_one:
                self.tail_form_one = float(self.tail_form_one)
            if self.tail_form_two:
                self.tail_form_two = float(self.tail_form_two)

            if self.other_pays:
                self.other_pays = [OtherPays(**other_pay) for other_pay in self.other_pays]
        except TypeError:
            serializers.ValidationError('wrong float data in tmp_multi')

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class ClientTailForm():
    """
    Form to payorder (cash or bank)
    """
    tail_form_one: str = "tail_form_one" 
    tail_form_two: str = "tail_form_two" 


@dataclass
class MessageUserForDealStatus():
    """
    For deal status
    """
    message: str
    owner: CustomUser | QuerySet[CustomUser] 

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class BaseMessageForm():
    """
    Base atr fo create message.
    """
    message: str
    model: Union[
        BuyerCardEggs, SellerCardEggs,
        LogicCardEggs, BaseDealEggsModel
    ]
    user: CustomUser | QuerySet[CustomUser]

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class AdditionalExpenseData():
    """
    Form for additional expense json.
    """
    comment: str
    date_time: str
    expence: str | float
    owner_name: str
    owner_id: str | int

    def __post_init__(self):
        try:
            self.expence = float(self.expence)
            self.owner_id = int(self.owner_id)
        except TypeError:
            serializers.ValidationError(
                'wrong float expens or user id in tmp_json')
    
    def __getitem__(self, item):
        return getattr(self, item)







