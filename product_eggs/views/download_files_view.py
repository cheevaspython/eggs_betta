from rest_framework import viewsets

from product_eggs.models.documents import DocumentsDealEggsModel
from product_eggs.services.documents.docs_get_link import parce_pk_data, \
    start_the_desired_getter_link


class DownloadViewSet(viewsets.ViewSet):
    queryset = DocumentsDealEggsModel.objects.all().select_related()

    def retrieve(self, request, pk, *args, **kwargs):
        pk_data = parce_pk_data(pk)
        return start_the_desired_getter_link(pk_data[0], pk_data[1], pk_data[2])

