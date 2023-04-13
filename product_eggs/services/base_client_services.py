from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from product_eggs.models.base_eggs import SellerCardEggs, BuyerCardEggs
    

def get_client_for_inn(entry_inn: str) -> Optional[SellerCardEggs | BuyerCardEggs]:
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

    raise serializers.ValidationError('inn client is invalid, check entry data')


def get_client_for_tail_pk(client_tail_pk: int) -> Optional[SellerCardEggs | BuyerCardEggs]:
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
