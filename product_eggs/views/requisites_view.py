from rest_framework import permissions, response, viewsets

from product_eggs.models.requisites import RequisitesEggs
from product_eggs.serializers.requisites_serializers import RequisitesSerializer


class RequisitesRetrieveAPIView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RequisitesEggs.objects.all()

    def retrieve(self, request, pk, *args, **kwargs):
        instance = RequisitesEggs.objects.get(inn=pk)
        serializer = RequisitesSerializer(instance)
        return response.Response(serializer.data)
