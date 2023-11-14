from typing import Any

from dataclasses import dataclass

from rest_framework import serializers

from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.models.tails import TailsContragentModelEggs
from users.models import CustomUser

CLIENT_TYPES = [
    'seller', 'buyer', 'logic',
]

DOCUMENT_TYPES = [
    'UPD_incoming', 'UPD_outgoing', 'UPD_logic', 'application_contract_logic',
    'payment_order_outcoming_logic', 'payment_order_outcoming', 'payment_order_incoming',
    'tail_payment', 'multi_pay_order',
]

TMP_DOCTYPE_BOOK = {
    'buyer': [
        'UPD_outgoing',
        'payment_order_incoming',
        'tail_payment',
        'multi_pay_order',
    ],
    'seller': [
        'UPD_incoming',
        'payment_order_outcoming',
        'tail_payment',
        'multi_pay_order',
    ],
    'logic': [
        'UPD_logic', 'application_contract_logic',
        'payment_order_outcoming_logic',
        'tail_payment',
        'multi_pay_order',
    ]
}

SELLER_DOCS = [
    'payment_order_outcoming', 'specification_seller', 'account_to_seller', 'UPD_incoming',
    'account_invoicing_from_seller', 'product_invoice_from_seller',
    'veterinary_certificate_seller', 'international_deal_TTN_seller', 'multi_pay_order',
]

BUYER_DOCS = [
    'payment_order_incoming', 'specification_buyer', 'account_to_buyer',
    'UPD_outgoing', 'account_invoicing_from_buyer', 'product_invoice_from_buyer',
    'veterinary_certificate_buyer', 'UPD_outgoing_signed', 'international_deal_TTN_buyer',
    'multi_pay_order',
]

LOGIC_DOCS = [
    'application_contract_logic', 'account_to_logic', 'UPD_logic',
    'account_invoicing_logic', 'product_invoice_logic', 'payment_order_outcoming_logic',
    'international_deal_CMR',  'multi_pay_order',
]

ENTITY_BOOK = [
    'test', 'test1', 'application_contract_logic_entity_empty'
]


@dataclass(slots=True)
class PrePayOrderDataForSave():
    """
    request data from front
    """
    date: str
    number: str
    pay_quantity: str
    inn: str
    doc_type: str
    client_type: str
    entity: str
    cash: bool
    force: bool = False

    def __post_init__(self):
        if self.doc_type == 'application_contract_logic':
            self.entity = 'application_contract_logic_entity_empty'
        else:
            if self.entity not in ENTITY_BOOK:
                raise serializers.ValidationError('wrong entity in tmp_json')
        if self.doc_type not in DOCUMENT_TYPES:
            raise serializers.ValidationError('wrong doc type in tmp_json')
        if self.client_type not in CLIENT_TYPES:
            raise serializers.ValidationError('wrong client type in tmp_json')
        if self.doc_type not in TMP_DOCTYPE_BOOK[self.client_type]:
            raise serializers.ValidationError('wrong doc type for current client type in tmp_json')

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True)
class TailTransactionData():
    """
    Tail for for transaction
    """
    tail: TailsContragentModelEggs
    delta: float
    pre_pay_data: PrePayOrderDataForSave
    uuid: str
    user: CustomUser
    doc_deal_pk: int

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True, frozen=True)
class PayOrderDataForSave():
    """
    Dataclass для упорядочивания данных,
    по финансовым документам, для сохранения в базу.
    """
    user: int
    date: str
    number: str
    pay_quantity: float
    inn: str
    deal: str
    doc_type: str
    entity: str
    documents_id: str
    client_type: str
    force: bool = False

    def __post_init__(self):
        if self.entity not in ENTITY_BOOK:
            raise serializers.ValidationError('wrong entity in tmp_json')
        if self.doc_type not in DOCUMENT_TYPES:
            raise serializers.ValidationError('wrong doc type in tmp_json')
        if self.client_type not in CLIENT_TYPES:
            raise serializers.ValidationError('wrong client type in tmp_json')
        else:
            if self.doc_type not in TMP_DOCTYPE_BOOK[self.client_type]:
                raise serializers.ValidationError('wrong doc type for current client type in tmp_json')

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass
class OtherPayTmpData():
    """
    Temporary data for cycle class MultyDocumentsPaymentParser
    Method -> splitter_multi_order
    """
    current_pay: Any
    construct: PayOrderDataForSave
    current_deal_doc: DocumentsDealEggsModel

    def __post_init__(self):
        from product_eggs.services.documents.documents_parse_tmp_json import DealDocumentsPaymentParser
        if not isinstance(self.current_pay, DealDocumentsPaymentParser):
            raise serializers.ValidationError(
                'wrong DealDocumentsPaymentParser model in Otherpays data_class')

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True)
class OtherPays():
    """
    Dataclass для упорядочивания данных,
    для общего платежного поручения,
    для поля со сделками.
    """
    deal_docs_pk: str
    pay_quantity: str | float

    def __post_init__(self):
        try:
            if not self.pay_quantity:
                raise serializers.ValidationError(
                    'Wrong pay_quantity in otherpays, pay_quantity cant be false')
            self.pay_quantity = float(self.pay_quantity)
        except KeyError as e:
            raise serializers.ValidationError('Wrong pay_quantity type in otherpays', e)

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True)
class PrePayOrderDataForSaveMulti():
    """
    data for MultyDocumentsPaymentParser entry
    """
    date: str
    number: str
    inn: str
    total_amount: str
    tail_form_one: str | None
    tail_form_two: str | None
    other_pays: list | dict
    doc_type: str
    client_type: str
    entity: str
    cash: bool = False

    def __post_init__(self):
        if self.entity not in ENTITY_BOOK:
            raise serializers.ValidationError('wrong entity in tmp_json')
        if self.doc_type not in DOCUMENT_TYPES:
            raise serializers.ValidationError('wrong doc type in tmp_json')
        if self.entity not in ENTITY_BOOK:
            raise serializers.ValidationError('wrong entity in tmp_json')

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True)
class PayOrderDataForSaveMulti():
    """
    Dataclass для упорядочивания данных,
    для общего платежного поручения.
    """
    user: int
    date: str
    number: str
    inn: str
    total_amount: str | float
    other_pays: list | dict
    client_type: str
    entity: str
    tail_form_one: str | float | None = None
    tail_form_two: str | float | None = None

    def __post_init__(self):
        if self.entity not in ENTITY_BOOK:
            raise serializers.ValidationError('wrong entity in tmp_json')
        try:
            self.total_amount = float(self.total_amount)
            if self.tail_form_one:
                self.tail_form_one = float(self.tail_form_one)
            if self.tail_form_two:
                self.tail_form_two = float(self.tail_form_two)
        except TypeError:
            raise serializers.ValidationError('PayOrderDataForSaveMulti: wrong tail form ')
        try:
            if isinstance(self.other_pays, dict):
                self.other_pays = [OtherPays(**self.other_pays)]
            elif isinstance(self.other_pays, list):
                self.other_pays = [OtherPays(**other_pay) for other_pay in self.other_pays]
            else:
                raise serializers.ValidationError('PayOrderDataForSaveMulti: wrong other_pays type')
        except TypeError:
            raise serializers.ValidationError('PayOrderDataForSaveMulti: wrong other_pays ')

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True, frozen=True)
class PayOrderDataForSaveMultiClear():
    """
    data for save, clear fields
    """
    user: int
    date: str
    number: str
    inn: str
    entity: str
    total_amount: float

    def __post_init__(self):
        if self.entity not in ENTITY_BOOK:
            raise serializers.ValidationError('wrong entity in tmp_json')

    def __getitem__(self, item):
        return getattr(self, item)


@dataclass(slots=True)
class MultiTails():
    """
    data for views tails
    """
    other_pays: list
    doc_type: str
    entity: str
    cash: bool = False
    total_pay: float = 0

    def __post_init__(self):
        if self.entity not in ENTITY_BOOK:
            raise serializers.ValidationError('wrong entity in tmp_json')
        if self.doc_type not in DOCUMENT_TYPES:
            raise serializers.ValidationError('wrong doc type in tmp_json')
        try:
            self.total_pay = sum([float(other['pay_quantity']) for other in self.other_pays])
            self.other_pays = [OtherPays(**other_pay) for other_pay in self.other_pays]
        except TypeError as e:
            raise serializers.ValidationError(
                'wrong data in MultiTails dataclass', e)

    def __getitem__(self, item):
        return getattr(self, item)








