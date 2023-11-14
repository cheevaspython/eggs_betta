from users.models import CustomUser

from django.core.exceptions import ObjectDoesNotExist

from product_eggs.models.base_client import BuyerCardEggs, SellerCardEggs


def get_managers(inn_seller: int, inn_buyer: int) -> list[CustomUser]:
    """
    Возвращает менеджеров по ИНН.
    """
    try:
        seller_manager = SellerCardEggs.objects.get(inn=inn_seller).manager
        buyer_manager = BuyerCardEggs.objects.get(inn=inn_buyer).manager
        if seller_manager and buyer_manager:
            return [seller_manager, buyer_manager]
        else:
            raise AttributeError('inn_seller or inn_buyer wrong')

    except ObjectDoesNotExist as e:
        raise AttributeError('inn_seller or inn_buyer wrong', e)


