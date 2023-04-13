from rest_framework import routers

from product_eggs.views.calc_views import CalculateEggsViewSet, ConfirmedCalculateEggsViewSet
        

calculate_eggs_router = routers.SimpleRouter()
calculate_eggs_router.register(r'', CalculateEggsViewSet)

confirmed_calculate_eggs_router = routers.SimpleRouter()
confirmed_calculate_eggs_router.register(r'', ConfirmedCalculateEggsViewSet)

