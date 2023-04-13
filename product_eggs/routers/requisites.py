from rest_framework import routers

from product_eggs.views.requisites_view import RequisitesRetrieveAPIView 


requisites_router = routers.SimpleRouter()
requisites_router.register(r'', RequisitesRetrieveAPIView)
