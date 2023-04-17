from typing import OrderedDict
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from product_eggs.models.tails import TailsContragentModelEggs
from product_eggs.permissions.validate_user import eq_requestuser_is_customuser
from product_eggs.serializers.tails_serializers import TailsEggsSerializer
from product_eggs.services.tails import check_validated_tails_data_for_fields, \
    transaction_tails_data, wrong_entry_tail_data


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
        instance = TailsContragentModelEggs.objects.get(pk=pk)  
        serializer = TailsEggsSerializer(instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)

        if isinstance(serializer.validated_data, OrderedDict):
            if check_validated_tails_data_for_fields(serializer.validated_data):
                wrong_entry_tail_data(serializer.validated_data)

                transaction_tails_data(
                    serializer.validated_data['tmp_json_for_multi_pay_order'],
                    instance,
                    eq_requestuser_is_customuser(self.request.user),
                    serializer.validated_data['tmp_key_form_dict'],
                )
                serializer.validated_data['tmp_json_for_multi_pay_order'] = {}
                serializer.validated_data['tmp_key_form_dict'] = {}
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)    








