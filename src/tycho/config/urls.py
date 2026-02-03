"""URL configuration for tycho project."""

from django.contrib import admin
from django.urls import include, path

from presentation.api import urls as api_urls

urlpatterns = [
    path("", include("presentation.pages.urls")),
    path("api/", include(api_urls)),
    path("admin/", admin.site.urls),
    path("candidate/", include("presentation.candidate.urls")),
    path("ingestion/", include("presentation.ingestion.urls")),
]
