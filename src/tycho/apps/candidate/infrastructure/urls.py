"""URL configuration for candidate app."""

from django.urls import path

from apps.candidate.infrastructure.adapters.website.views import (
    CorpsSearchView,
    HomeView,
)

app_name = "candidate"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search/", CorpsSearchView.as_view(), name="search"),
]
