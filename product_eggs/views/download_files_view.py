from rest_framework import viewsets

from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.services.documents.docs_get_link import DownloadDocumentsLink


class DownloadViewSet(viewsets.ViewSet):
    queryset = DocumentsDealEggsModel.objects.all()

    def retrieve(self, request, pk, *args, **kwargs):
        return DownloadDocumentsLink(pk).get_auto_download_response()

