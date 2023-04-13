from rest_framework import routers

from product_eggs.views.limit_duty_eggs import LimitDutyEggsViewSet 
from product_eggs.views.limit_duty_eggs import BalanceSellerEggs 


limit_duty_eggs_router = routers.SimpleRouter()
limit_duty_eggs_router.register(r'', LimitDutyEggsViewSet)

balance_seller_eggs_router = routers.SimpleRouter()
balance_seller_eggs_router.register(r'', BalanceSellerEggs)
