from users.models import CustomUser
from product_eggs.models.base_eggs import BuyerCardEggs, SellerCardEggs


def get_managers(inn_seller: int, inn_buyer: int) -> list[CustomUser]:
    """
    Возвращает менеджеров по ИНН.
    """
    seller_manager = SellerCardEggs.objects.get(inn=inn_seller).manager
    buyer_manager = BuyerCardEggs.objects.get(inn=inn_buyer).manager
    return [seller_manager, buyer_manager]

