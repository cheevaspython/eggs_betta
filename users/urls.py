from django.urls import path, include

from users.routers import user_detail_router
from users.views import WhoamiApiView


urlpatterns = [
    path('users_list/', include(user_detail_router.urls)),
    path('whoami/', WhoamiApiView.as_view()),
]


