from rest_framework import routers

from product_eggs.views.comments_view import CommentsEggsModelViewSet

comments_router = routers.SimpleRouter()
comments_router.register(r'', CommentsEggsModelViewSet)
