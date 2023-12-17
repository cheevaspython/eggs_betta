from collections import OrderedDict
from rest_framework.decorators import action
from rest_framework import permissions, viewsets
from rest_framework.response import Response

from product_eggs.models.base_deal import BaseDealEggsModel
from product_eggs.serializers.personal_area_serializers import DataForPersonAreaSerializer
from product_eggs.services.personal_area import PersonalSalaryBalanceService
from users.models import CustomUser

current_active_entitys = [
    '5612163931', '5048057438',
]

class PersonalAreaModelViewSet(viewsets.ViewSet):
    queryset = BaseDealEggsModel.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['patch'])
    def get_personal_wage_balance(self, request, pk=None) -> Response:
        serializer = DataForPersonAreaSerializer(
            data=request.data, partial=True
        )
        serializer.is_valid()
        if isinstance(serializer.validated_data, OrderedDict):
            if isinstance(self.request.user, CustomUser):
                personal_balanse_service = PersonalSalaryBalanceService(
                    serializer.validated_data['start_date'],
                    serializer.validated_data['end_date'],
                    self.request.user,
                    current_active_entitys,
                )
                result = personal_balanse_service.main()
                print(result)

                return Response(result)
        return Response('')
