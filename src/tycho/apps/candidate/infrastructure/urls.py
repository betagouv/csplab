"""URL configuration for candidate app."""

from django.urls import path

from apps.candidate.infrastructure.adapters.website.views import CorpsSearchView

app_name = "candidate"

urlpatterns = [
    path("search/", CorpsSearchView.as_view(), name="search"),
    path("", CorpsSearchView.as_view(), name="index"),
]
