from rest_framework import views, viewsets, permissions
from rest_framework.response import Response

from product_eggs.models.messages import MessageToUserEggs
from product_eggs.serializers.messages_serializers import MessageToUserEggsSerializer


class MessageToUserEggsModelViewSet(viewsets.ModelViewSet):   #TODO mb del?
    queryset = MessageToUserEggs.objects.all().select_related(
        'current_base_deal',
        'current_seller',
        'current_buyer',
        'current_logic',
        'message_to',
    )
    serializer_class = MessageToUserEggsSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class RequestUserMessage(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        messages = MessageToUserEggs.objects.filter(is_active=True).select_related(
            'current_base_deal',
            'current_seller',
            'current_buyer',
            'current_logic',
            'message_to',
        ).filter(message_to=request.user)

        serializer = MessageToUserEggsSerializer(messages, many=True)
        sort_data = sorted(serializer.data, key=lambda x: x['id'], reverse=True)
        return Response(sort_data)

