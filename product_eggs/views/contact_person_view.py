from rest_framework import permissions, serializers, response, status

from product_eggs.models.contact_person import ContactPersonEggs
from product_eggs.models.custom_model_viewset import CustomModelViewSet
from product_eggs.serializers.contact_person_serializers import ContactPersonEggsSerializer, InnTypeClientSerializer
from product_eggs.services.get_anything.try_to_get_models import get_client_for_inn


class ContactPersonView(CustomModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ContactPersonEggs.objects.all()
    serializer_class = ContactPersonEggsSerializer
    http_method_names = ['get', 'post', 'patch']
    cur_client = None

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer_inn_data = InnTypeClientSerializer(data=request.data)
        serializer_inn_data.is_valid(raise_exception=True)
        self.cur_client = get_client_for_inn(
            serializer_inn_data.data['client_inn'],
            serializer_inn_data.data['client_type'],
        )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return response.Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()
        instance = ContactPersonEggs.objects.get(pk=serializer.data['id'])
        if self.cur_client:
            self.cur_client.contact_person.add(instance)
            self.cur_client.save()


