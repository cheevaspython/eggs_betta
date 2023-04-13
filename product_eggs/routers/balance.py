from rest_framework import routers

from product_eggs.views.balance_view import BalanceEggsViewSet


balance_router = routers.SimpleRouter()
balance_router.register(r'', BalanceEggsViewSet)
