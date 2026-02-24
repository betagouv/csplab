"""URL configuration for pages."""

from django.urls import path

from presentation.pages.views import (
    HomeView,
    LegalNoticesView,
)

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("mentions-legales", LegalNoticesView.as_view(), name="legal_notices"),
]
