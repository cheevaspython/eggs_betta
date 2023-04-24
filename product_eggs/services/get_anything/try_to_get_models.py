from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from product_eggs.models.base_client import LogicCardEggs, SellerCardEggs, BuyerCardEggs
from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.services.decorators import try_decorator_param
    

def get_client_for_inn(
        entry_inn: str,
        ) -> Optional[SellerCardEggs | BuyerCardEggs | LogicCardEggs]:
    """ 
    Получает модель клиента по ИНН,
    raise exception в случае если ИНН не числится в базе.
    """
    try:
        seller = SellerCardEggs.objects.get(inn=entry_inn)
        return seller
    except ObjectDoesNotExist:
        pass
    try:
        buyer = BuyerCardEggs.objects.get(inn=entry_inn)
        return buyer
    except ObjectDoesNotExist:
        pass
    try:
        logic = LogicCardEggs.objects.get(inn=entry_inn)
        return logic
    except ObjectDoesNotExist:
        pass

    raise serializers.ValidationError('inn client/logic is invalid, check entry data')


def get_client_for_tail_pk(
        client_tail_pk: int) -> Optional[SellerCardEggs | BuyerCardEggs]:
    """ 
    Получает модель клиента по tails_id,
    raise exception в случае если ИНН не числится в базе.
    """
    try:
        seller = SellerCardEggs.objects.get(tails=client_tail_pk)
        return seller
    except ObjectDoesNotExist:
        pass
    try:
        buyer = BuyerCardEggs.objects.get(tails=client_tail_pk)
        return buyer
    except ObjectDoesNotExist:
        pass

    raise serializers.ValidationError('tail_pk for client_model is invalid, \
        check entry data')

            
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

