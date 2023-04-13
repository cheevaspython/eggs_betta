from rest_framework import views, response, permissions

from product_eggs.serializers.activefieldoffer_serializer import FieldIsActiveOfferSerializer
from product_eggs.services.turn_off_fields import field_is_active_offer_for_title_search


class FieldIsActiveOffApiview(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = FieldIsActiveOfferSerializer(request.data)
        field_is_active_offer_for_title_search(serializer.data['model_title'], serializer.data['model_id'])
        return response.Response('field OFF')
