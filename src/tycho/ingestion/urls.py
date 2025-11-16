"""URL configuration for ingestion app."""

from django.urls import path

from .views import CorpsETLView

urlpatterns = [
    path("etl/corps/", CorpsETLView.as_view(), name="corps-etl"),
]
