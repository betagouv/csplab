"""URL configuration for tycho project."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ingestion/", include("ingestion.urls")),  # ← Ajouter cette ligne
]
