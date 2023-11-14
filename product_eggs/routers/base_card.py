from rest_framework import routers

from product_eggs.views.client_card_view import (
    BuyerCardEggsViewSet, SellerCardEggsViewSet,
    LogicCardEggsViewSet, GetUserCardEggsViewSet,
)

buyer_card_eggs_router = routers.SimpleRouter()
buyer_card_eggs_router.register(r'', BuyerCardEggsViewSet)

seller_card_eggs_router = routers.SimpleRouter()
seller_card_eggs_router.register(r'', SellerCardEggsViewSet)

logic_card_eggs_router = routers.SimpleRouter()
logic_card_eggs_router.register(r'', LogicCardEggsViewSet)

guest_card_eggs_router = routers.SimpleRouter()
guest_card_eggs_router.register(r'', GetUserCardEggsViewSet)
