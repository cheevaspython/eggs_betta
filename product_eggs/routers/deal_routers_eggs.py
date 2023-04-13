from rest_framework import routers

from product_eggs.views.deal_views import DealEggsViewSet


deal_eggs_router = routers.SimpleRouter()
deal_eggs_router.register(r'', DealEggsViewSet)

