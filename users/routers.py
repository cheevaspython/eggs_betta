from rest_framework import routers

from users.views import UserViewSet


user_detail_router = routers.SimpleRouter()
user_detail_router.register(r'', UserViewSet)
