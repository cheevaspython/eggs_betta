from rest_framework import routers

from product_eggs.views.personal_area_view import PersonalAreaModelViewSet

personal_area_router = routers.SimpleRouter()
personal_area_router.register(r'', PersonalAreaModelViewSet)
