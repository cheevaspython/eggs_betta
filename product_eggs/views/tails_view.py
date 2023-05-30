import logging

from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.serializers.tails_serializers import TailsEggsSerializer
from product_eggs.services.data_class.data_class_documents import MultiTails
from product_eggs.services.tails_recoursia import tail_pay_recoursia

logger = logging.getLogger(__name__)


class TailsEggsViewSet(viewsets.ViewSet):
    queryset = TailsContragentModelEggs.objects.all()
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def get_tail(self, request, pk=None) -> Response:
        instance = TailsContragentModelEggs.objects.get(pk=pk)  
        serializer = TailsEggsSerializer(instance) 
        return Response(serializer.data, status=status.HTTP_200_OK)    

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def pay_tails(self, request, pk=None) -> Response:
        
        instance = self.queryset.get(pk=pk)  
        serializer = TailsEggsSerializer(
            instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if instance.multi_tails: 
            multi_tails = MultiTails(**instance.multi_tails)
            if multi_tails.form_type:
                for cur_pay in multi_tails.other_pays:
                    tail_pay_recoursia(
                        instance.pk,
                        cur_pay,
                        eq_requestuser_is_customuser(self.request.user),
                        form_type=multi_tails.form_type)

        instance = self.queryset.get(pk=pk)  
        instance.multi_tails = {}
        instance.save()

        return Response(serializer.data, status=status.HTTP_200_OK)    

