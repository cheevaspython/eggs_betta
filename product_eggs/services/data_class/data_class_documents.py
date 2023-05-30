from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from rest_framework import serializers
from product_eggs.models.documents import DocumentsDealEggsModel

from users.models import CustomUser
        

@dataclass
class OtherPayTmpData():
    """
    Temporary data for cycle class MultyDocumentsPaymentParser
    Method -> splitter_multi_order 
    """
    current_pay: Any 
    construct: dict
    current_deal_doc: DocumentsDealEggsModel
    
    def __post_init__(self):
        from product_eggs.services.documents.documents_parse_tmp_json \
            import DealDocumentsPaymentParser
        if not isinstance(self.current_pay, DealDocumentsPaymentParser):
            raise serializers.ValidationError(
                'wrong DealDocumentsPaymentParser model in Otherpays data_class')

    def __getitem__(self, item):
        return getattr(self, item)


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
    force: bool = False

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
    doc_type: str

    def __post_init__(self):
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
    date: str
    number: str
    inn: str
    total_amount: str | float
    tail_form_one: str | float | None
    tail_form_two: str | float | None
    other_pays: list | dict 

    def __post_init__(self):
        try:
            self.total_amount = float(self.total_amount)
            if self.tail_form_one:
                self.tail_form_one = float(self.tail_form_one)
            if self.tail_form_two:
                self.tail_form_two = float(self.tail_form_two)
            if self.other_pays:
                if isinstance(self.other_pays, dict):
                    self.other_pays = [OtherPays(**self.other_pays)]
                else:
                    self.other_pays = [OtherPays(**other_pay) for other_pay in self.other_pays]
        except TypeError:
            raise serializers.ValidationError('PayOrderDataForSaveMulti: wrong float/other_pays')

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class MultiTails():
    cash: bool
    other_pays: list
    total_pay: float = 0
    form_type: str | None = None 

    def __post_init__(self):
        try:
            self.total_pay = sum([float(other['pay_quantity']) for other in self.other_pays])
            self.other_pays = [OtherPays(**other_pay) for other_pay in self.other_pays]
            self.form_type = 'form_two' if self.cash else 'form_one'

        except TypeError:
            raise serializers.ValidationError(
                'wrong data in MultiTails dataclass')
    
    def __getitem__(self, item):
        return getattr(self, item)








