from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from presentation.api.views import HueyHealthView, RedocView
from presentation.ingestion.views import ArchiveOffersView

app_name = "api"

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("health/huey/", HueyHealthView.as_view(), name="health_huey"),
    path("schema/redoc/", RedocView.as_view(), name="redoc"),
    path(
        "offers/<str:reference>/archive/",
        ArchiveOffersView.as_view(),
        name="offers_archive",
    ),
]
