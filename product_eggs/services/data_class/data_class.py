from dataclasses import dataclass
from datetime import datetime
from typing import Union

from django.db.models import QuerySet
from rest_framework import serializers

from product_eggs.models.applications import ApplicationFromBuyerBaseEggs, \
    ApplicationFromSellerBaseEggs
from product_eggs.models.base_client import BuyerCardEggs, \
    LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.services.data_class.data_class_documents import OtherPays
from users.models import CustomUser


@dataclass(slots=True)
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
        LogicCardEggs, BaseDealEggsModel,
        ApplicationFromBuyerBaseEggs,
        ApplicationFromSellerBaseEggs,
    ]
    user: CustomUser | QuerySet[CustomUser]
    info: bool = False
    done: bool = False

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class AdditionalExpenseData():
    """
    Form for additional expense json.
    """
    comment: str
    date_time: str
    expense: str | float
    owner_name: str
    owner_id: str | int

    def __post_init__(self):
        try:
            self.expense = float(self.expense)
            self.owner_id = int(self.owner_id)
        except TypeError:
            raise serializers.ValidationError(
                'wrong float expens or user id in tmp_json')
    
    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True)
class TailTransactionData():

    date: str | None
    number: str
    inn: str
    total_amount: float 
    tail_form_one: float | None 
    tail_form_two: float | None
    other_pays: OtherPays        

    def __post_init__(self):
        self.date = datetime.now().date().strftime('%d/%m/%Y')
        try: 
            float(self.total_amount)
            isinstance(self.other_pays, OtherPays)
        except [TypeError, ValueError]:
            raise serializers.ValidationError('wrong type in TailTransactionData')
    
    def __getitem__(self, item):
        return getattr(self, item)









