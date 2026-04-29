"""URL configuration for pages."""

from django.urls import path

from presentation.pages.views import (
    HomeView,
    PrivacyView,
)

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("confidentialite", PrivacyView.as_view(), name="privacy"),
]
