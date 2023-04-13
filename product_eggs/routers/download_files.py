from rest_framework import routers

from product_eggs.views.download_files_view import DownloadViewSet
        

download_router = routers.SimpleRouter()
download_router.register(r'', DownloadViewSet)
