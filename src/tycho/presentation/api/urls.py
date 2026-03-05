"""URL configuration for third parties API."""

from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from presentation.api.views import StaticSchemaView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("schema/", StaticSchemaView.as_view(), name="schema"),
    path(
        "docs/",
        TemplateView.as_view(
            template_name="api/swagger_ui.html",
            extra_context={"schema_url": "/api/schema/"},
        ),
        name="swagger-ui",
    ),
]
