from django.urls import path
from drf_spectacular.views import SpectacularAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from presentation.api.views import HueyHealthView, RedocView

app_name = "api"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("health/huey/", HueyHealthView.as_view(), name="health_huey"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("schema/redoc/", RedocView.as_view(), name="redoc"),
]
