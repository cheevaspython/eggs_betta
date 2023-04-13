from typing import OrderedDict
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from product_eggs.serializers.additional_expense_serializers import \
    AdditionalExpenseSerializer
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.services.additional_exp_service import parse_additional_tmp_json


class AdditionalExpenseEggsModelViewSet(viewsets.ViewSet):
    queryset = AdditionalExpenseEggs.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = AdditionalExpenseSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

    @action(detail=True, methods=['get'])
    def update_expense(self, request, pk=None) -> Response:  
        instance = AdditionalExpenseEggs.objects.get(pk=pk)
        serializer = AdditionalExpenseSerializer(
            instance, data=request.data, partial=True) 
        serializer.is_valid()

        if isinstance(serializer.validated_data, OrderedDict):
            if data_for_save := parse_additional_tmp_json(
                    serializer.validated_data):

                serializer.save()
                instance.expense_detail_json.update(
                    data_for_save)
                instance.expense_total += data_for_save.expence
                instance.save()
                return Response(
                    serializer.data, status=status.HTTP_200_OK)    

        return Response('Wrong tmp_json')





 
