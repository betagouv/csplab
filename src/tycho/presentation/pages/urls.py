"""URL configuration for pages."""

from django.urls import path

from presentation.pages.views import (
    AccessibilityView,
)

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("accessibilite", AccessibilityView.as_view(), name="accessibility"),
]
