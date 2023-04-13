from rest_framework import routers

from product_eggs.views.documents_view import DocumentsViewSet
        

documents_router = routers.SimpleRouter()
documents_router.register(r'', DocumentsViewSet)
