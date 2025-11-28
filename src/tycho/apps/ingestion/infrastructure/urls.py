"""URL configuration for ingestion app."""

from django.urls import path

from apps.ingestion.infrastructure.adapters.api.views import LoadDocumentsView

urlpatterns = [
    path("load/", LoadDocumentsView.as_view(), name="load-documents"),
]
