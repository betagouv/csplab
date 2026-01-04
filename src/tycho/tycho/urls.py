"""URL configuration for tycho project."""

from django.contrib import admin
from django.urls import include, path

from apps.candidate.infrastructure.adapters.website.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("ingestion/", include("apps.ingestion.infrastructure.urls")),
    path("candidate/", include("apps.candidate.infrastructure.urls")),
]
