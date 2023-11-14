from rest_framework import routers

from product_eggs.views.tails_view import TailsEggsViewSet

tails_router = routers.SimpleRouter()
tails_router.register(r'', TailsEggsViewSet)
