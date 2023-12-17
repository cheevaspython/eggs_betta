from dataclasses import dataclass
from typing import Union

from django.db.models import QuerySet

from product_eggs.models.applications import  (
    ApplicationFromBuyerBaseEggs, ApplicationFromSellerBaseEggs
)
from product_eggs.models.base_client import (
    BuyerCardEggs, LogicCardEggs, SellerCardEggs
)
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsContractEggsModel
from product_eggs.services.data_class.data_class_documents import PrePayOrderDataForSaveMulti
from product_eggs.services.validationerror import custom_error
from users.models import CustomUser

COMMENT_MODEL_TYPES = (
    'app_seller', 'app_buyer', 'base_deal'
)

DELETE_CLIENT_MODELS = (
    'seller', 'buyer', 'logic'
)
ENTITY_BOOK = [
    '5612163931', '5048057438', 'application_contract_logic_entity_empty'
]


@dataclass(slots=True)
class ClientTailForm():
    """
    Form to payorder (cash or bank)
    """
    tail_form_one: str = "tail_form_one"
    tail_form_two: str = "tail_form_two"


@dataclass(slots=True)
class MessageUserForDealStatus():
    """
    For deal status
    """
    message: str
    owner: CustomUser | QuerySet[CustomUser]

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True)
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


@dataclass(slots=True)
class AdditionalExpenseData():
    """
    Form for additional expense json.
    """
    comment: str
    date_time: str
    expense: str | float
    owner_name: str
    owner_id: str | int
    cash: bool
    logic: bool | None = None

    def __post_init__(self):
        try:
            self.expense = float(self.expense)
            self.owner_id = int(self.owner_id)
        except TypeError:
            raise custom_error(
                'wrong float expens or user id in tmp_json', 433)

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True)
class CommentData():
    """
    Form for comment json.
    """
    owner_id: int
    owner_name: str
    comment: str
    model_id: int
    model_type: str
    date_time: str | None

    def __post_init__(self):
        if self.model_type not in COMMENT_MODEL_TYPES:
            raise custom_error('model_type in comment data', 433)

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True)
class TailMultiData():
    """
    Tail data for MultiDocumentsPaymentParser
    """
    pre_order_data: PrePayOrderDataForSaveMulti
    documents_contract: DocumentsContractEggsModel
    cash: bool

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True, frozen=True)
class TailDataForJsonSave():
    """
    Tail data for tail_dict_json
    """
    user: int
    date: str
    number: str
    pay_quantity: float
    entity: str

    def __post_init__(self):
        if self.entity not in ENTITY_BOOK:
            raise custom_error('wrong entity in tmp_json', 433)

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True, frozen=True)
class DeleteJson():
    """
    Data for delete
    """
    json_key: str
    cash: bool
    client_type: str

    def __post_init__(self):
        if self.client_type not in DELETE_CLIENT_MODELS:
            raise custom_error('wrong client_type in delete dataclass', 433)

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True, frozen=True)
class GetWageJson():
    """
    For get wage field in personalbalance
    """
    wage_quantity: float
    wage_text: str

    def __post_init__(self):
        if self.wage_quantity <= 0:
            raise custom_error('wage must be correct', 433)

    def __getitem__(self, item):
        return getattr(self, item)


