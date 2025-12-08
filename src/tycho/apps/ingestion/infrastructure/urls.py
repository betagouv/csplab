"""URL configuration for ingestion app."""

from django.urls import path

from apps.ingestion.infrastructure.adapters.api.views import (
    ConcoursUploadView,
    LoadDocumentsView,
)

urlpatterns = [
    path("load/", LoadDocumentsView.as_view(), name="load-documents"),
    path("concours/upload/", ConcoursUploadView.as_view(), name="concours-upload"),
]
