"""URL configuration for pages."""

from django.urls import path

from presentation.pages.views import (
    HomeView,
    TermsView,
)

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("conditions-generales", TermsView.as_view(), name="terms"),
]
