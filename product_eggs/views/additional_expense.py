from rest_framework import viewsets, response, permissions

from product_eggs.serializers.additional_expense_serializer import AdditionalExpenseEggsDetailSerializer,\
    AdditionalExpenseEggsSerializer
from product_eggs.models.additional_expense import AdditionalExpenseEggs


class AdditionalExpenseEggsModelViewSet(viewsets.ViewSet):
    queryset = AdditionalExpenseEggs.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        serializer = AdditionalExpenseEggsDetailSerializer(self.queryset, many=True)
        return response.Response(serializer.data) 

    def patch(self, request):
        serializer = AdditionalExpenseEggsSerializer(data=request.data)
        serializer.is_valid()
        instance = AdditionalExpenseEggs.objects.get(id=serializer.data['model_id']) 
        instance.expense_detail_json.update(serializer.data['expense_detail_json_pre'])
        instance.expense_total += serializer.data['expense']
        instance.save()
        return response.Response('serialize update')






 
