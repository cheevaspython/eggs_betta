from rest_framework import routers

from product_eggs.views.balance_view import BalanceEggsViewSet, BalanceEggsModelViewSet

balance_router = routers.SimpleRouter()
balance_router.register(r'', BalanceEggsViewSet)

balance_model_router = routers.SimpleRouter()
balance_model_router.register(r'', BalanceEggsModelViewSet)
