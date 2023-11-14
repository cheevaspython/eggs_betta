from rest_framework import viewsets, permissions, response, views

from users.models import CustomUser
from users.serializers import CustomUserSerializer, CheckMasterPasswordSerializer
from users.services import master_pass_validate


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class WhoamiApiView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        response_dict = {
                "user_id" : request.user.id,
                "user_role": request.user.role,
                "user_first_name": request.user.first_name,
                "user_last_name": request.user.last_name
        }
        return response.Response(response_dict)

    def post(self, request):
        serializer = CheckMasterPasswordSerializer(data=request.data)
        serializer.is_valid()
        if master_pass_validate(serializer.data, request.user):
            return response.Response({"entered_password": True})
        return response.Response({"entered_password": False})


