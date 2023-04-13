from rest_framework import routers

from product_eggs.views.base_deal_view import BaseDealModelViewSet


base_deal_router = routers.SimpleRouter()
base_deal_router.register(r'', BaseDealModelViewSet)
