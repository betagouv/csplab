from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from presentation.api.token_views import LoggedTokenObtainPairView
from presentation.api.views import HueyHealthView, RedocView

app_name = "api"

urlpatterns = [
    path("token", LoggedTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("health/huey", HueyHealthView.as_view(), name="health_huey"),
    path("schema/redoc", RedocView.as_view(), name="redoc"),
]
