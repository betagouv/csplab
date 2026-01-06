"""URL configuration for pages."""

from django.urls import path

from presentation.pages.views import HomeView

app_name = "pages"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
