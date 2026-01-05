"""URL configuration for ingestion app."""

from django.urls import path

from presentation.ingestion.views import ConcoursUploadView

urlpatterns = [
    path("concours/upload/", ConcoursUploadView.as_view(), name="concours-upload"),
]
