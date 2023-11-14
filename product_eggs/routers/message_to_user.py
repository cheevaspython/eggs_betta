from rest_framework import routers

from product_eggs.views.messages_view import MessageToUserEggsModelViewSet

messages_to_users_router = routers.SimpleRouter()
messages_to_users_router.register(r'', MessageToUserEggsModelViewSet)
