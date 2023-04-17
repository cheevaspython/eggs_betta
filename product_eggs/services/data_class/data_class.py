from dataclasses import dataclass
from typing import Union

from django.db.models import QuerySet
from rest_framework import serializers

from product_eggs.models.base_client import BuyerCardEggs, LogicCardEggs, SellerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from users.models import CustomUser


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
    expense: str | float
    owner_name: str
    owner_id: str | int

    def __post_init__(self):
        try:
            self.expense = float(self.expense)
            self.owner_id = int(self.owner_id)
        except TypeError:
            serializers.ValidationError(
                'wrong float expens or user id in tmp_json')
    
    def __getitem__(self, item):
        return getattr(self, item)

