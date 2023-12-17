from dataclasses import asdict
from datetime import datetime
from typing import OrderedDict

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from product_eggs.serializers.additional_expense_serializers import (
    AdditionalExpenseSerializer
)
from product_eggs.models.additional_expense import AdditionalExpenseEggs
from product_eggs.services.additional_exp_service import (
    parse_additional_tmp_json, parse_additional_tmp_multi_json
)


class AdditionalExpenseEggsModelViewSet(viewsets.ViewSet):
    queryset = AdditionalExpenseEggs.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = AdditionalExpenseSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'])
    def update_expense(self, request, pk=None) -> Response:
        instance = AdditionalExpenseEggs.objects.get(pk=pk)
        serializer = AdditionalExpenseSerializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid()

        if isinstance(serializer.validated_data, OrderedDict):
            if data_for_save := parse_additional_tmp_json(
                    serializer.validated_data):

                serializer.save()
                if data_for_save.logic:
                    instance.expense_detail_json.update(
                        {str(datetime.today()) : asdict(data_for_save)}
                    )
                    instance.logic_pay = float(data_for_save.expense)
                else:
                    instance.expense_detail_json.update(
                        {str(datetime.today()) : asdict(data_for_save)}
                    )
                    if data_for_save.cash:
                        instance.expense_total_form_2 += float(data_for_save.expense)
                    else:
                        instance.expense_total_form_1 += float(data_for_save.expense)

                instance.tmp_json = {}
                instance.save()
                return Response(status=status.HTTP_200_OK)

            elif parse_additional_tmp_multi_json(instance, serializer.validated_data):
                return Response(status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response(status=status.HTTP_200_OK)

        return Response('Wrong tmp_json', status=status.HTTP_400_BAD_REQUEST)






