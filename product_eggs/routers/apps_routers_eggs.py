from rest_framework import routers

from product_eggs.views.apps_views import ApplicationBuyerEggsViewSet, ApplicationSellerEggsViewSet


application_from_buyer_router = routers.SimpleRouter()
application_from_buyer_router.register(r'', ApplicationBuyerEggsViewSet)

application_from_seller_router = routers.SimpleRouter()
application_from_seller_router.register(r'', ApplicationSellerEggsViewSet)


