"""URL configuration for candidate app."""

from django.urls import path

from presentation.candidate.views.corps_search import CorpsSearchView

app_name = "candidate"

urlpatterns = [
    path("", CorpsSearchView.as_view(), name="index"),
]
