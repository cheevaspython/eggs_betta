from rest_framework import routers

from product_eggs.views.requisites_view import RequisitesModelViewSet

requisites_router = routers.SimpleRouter()
requisites_router.register(r'', RequisitesModelViewSet)
