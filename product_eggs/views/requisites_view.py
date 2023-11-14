from rest_framework import permissions

from product_eggs.models.custom_model_viewset import CustomModelViewSet
from product_eggs.models.requisites import RequisitesEggs
from product_eggs.serializers.requisites_serializers import RequisitesEggsModelSerializer


class RequisitesModelViewSet(CustomModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = RequisitesEggs.objects.all()
    serializer_class = RequisitesEggsModelSerializer
    http_method_names = ['get', 'post', 'patch']


