from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from product_eggs.models.balance import BalanceBaseClientEggs

from product_eggs.models.base_client import LogicCardEggs, SellerCardEggs, BuyerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsContractEggsModel, DocumentsDealEggsModel
from product_eggs.services.balance import get_balance_for_tail_pk
from product_eggs.services.decorators import try_decorator_param

CLIENT_TYPES_BOOK = {
    'seller': 'SellerCardEggs',
    'buyer': 'BuyerCardEggs',
    'logic': 'LogicCardEggs',
}

CLIENT_TYPES_BOOK_REVERSE = {
    'SellerCardEggs': 'seller',
    'BuyerCardEggs': 'buyer',
    'LogicCardEggs': 'logic',
}


def get_client_for_inn(
        entry_inn: str, client_type,
        ) -> Optional[SellerCardEggs | BuyerCardEggs | LogicCardEggs]:
    """
    Получает модель клиента по ИНН,
    raise exception в случае если ИНН не числится в базе.
    """
    match client_type:
        case 'seller':
            try:
                seller = SellerCardEggs.objects.get(inn=entry_inn)
                return seller
            except ObjectDoesNotExist:
                pass
        case 'buyer':
            try:
                buyer = BuyerCardEggs.objects.get(inn=entry_inn)
                return buyer
            except ObjectDoesNotExist:
                pass
        case 'logic':
            try:
                logic = LogicCardEggs.objects.get(inn=entry_inn)
                return logic
            except ObjectDoesNotExist:
                pass
        case _:
            print('client_type is wrong')

    raise serializers.ValidationError('inn client/logic is invalid, check entry data')


def get_client_for_doc_contract(
        model: DocumentsContractEggsModel,
        client_type,
        ) -> SellerCardEggs | BuyerCardEggs | LogicCardEggs:
    """
    Получает модель клиента по ИНН,
    raise exception в случае если ИНН не числится в базе.
    """
    match client_type:
        case 'seller':
            try:
                seller = SellerCardEggs.objects.get(documents_contract=model.pk)
                return seller
            except ObjectDoesNotExist:
                pass
        case 'buyer':
            try:
                buyer = BuyerCardEggs.objects.get(documents_contract=model.pk)
                return buyer
            except ObjectDoesNotExist:
                pass
        case 'logic':
            try:
                logic = LogicCardEggs.objects.get(documents_contract=model.pk)
                return logic
            except ObjectDoesNotExist:
                pass
        case _:
            print('client_type is wrong')

    raise serializers.ValidationError('doc_contract_id is invalid, check entry data')


def get_client_for_tail_pk(
        client_tail_pk: int) -> SellerCardEggs | BuyerCardEggs | LogicCardEggs:
    """
    Получает модель клиента по tails_id,
    raise exception в случае если pk не числится в базе.
    """
    cur_balance = get_balance_for_tail_pk(client_tail_pk)

    if cur_balance.client_buyer:
        return cur_balance.client_buyer
    elif cur_balance.client_seller:
        return cur_balance.client_seller
    elif cur_balance.client_logic:
        return cur_balance.client_logic
    else:
        raise serializers.ValidationError(
            'tail_pk for client_model is invalid, check entry data')


@try_decorator_param(('KeyError',))
def try_to_get_deal_model(deal_id: int) -> BaseDealEggsModel:
    """
    Получает модель сделки по pk.
    """
    return BaseDealEggsModel.objects.get(pk=deal_id)


@try_decorator_param(('KeyError',))
def try_to_get_deal_model_for_doc_deal_id(doc_deal_id: int) -> BaseDealEggsModel:
    """
    Получает модель сделки по pk документов к сделке.
    """
    return BaseDealEggsModel.objects.get(documents=doc_deal_id)


@try_decorator_param(('KeyError',))
def try_to_get_deal_docs_model(docs_id: int) -> DocumentsDealEggsModel:
    """
    Получает модель документов к сделке по pk.
    """
    return DocumentsDealEggsModel.objects.get(pk=docs_id)


def check_client_type_and_model(client: SellerCardEggs | BuyerCardEggs | LogicCardEggs, client_type: str) -> None:
    """
    Сравнивает указанный тип и самого клиента.
    """
    if client_type not in CLIENT_TYPES_BOOK.keys():
        raise serializers.ValidationError('wrong client type')
    if CLIENT_TYPES_BOOK[client_type] != client.__class__.__name__:
        raise serializers.ValidationError('client type not valid for client model')


def return_client_type(client: SellerCardEggs | BuyerCardEggs | LogicCardEggs) -> str:
    return CLIENT_TYPES_BOOK_REVERSE[client.__class__.__name__]


def get_balance_model_for_client_and_entity(client_inn: str, entity_inn: str) -> BalanceBaseClientEggs:
    try:
        return BalanceBaseClientEggs.objects.get(client_buyer=client_inn, entity__inn=entity_inn)
    except ObjectDoesNotExist:
        pass
    try:
        return BalanceBaseClientEggs.objects.get(client_seller=client_inn, entity__inn=entity_inn)
    except ObjectDoesNotExist:
        pass
    try:
        return BalanceBaseClientEggs.objects.get(client_logic=client_inn, entity__inn=entity_inn)
    except ObjectDoesNotExist:
        pass

    raise serializers.ValidationError('inn client+entity: wrong in get_balance_model_for_client_and_entity')



