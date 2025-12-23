"""URL configuration for candidate app."""

from django.urls import path

from apps.candidate.infrastructure.adapters.website.views import (
    CorpsSearchView,
    CVConfirmationView,
    CVUploadView,
    HomeView,
    OpportuniteDetailView,
    ResultatsAnalyseView,
)

app_name = "candidate"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search/", CorpsSearchView.as_view(), name="search"),
    path("cv-upload/", CVUploadView.as_view(), name="cv_upload"),
    path(
        "cv/<uuid:cv_id>/confirmation/",
        CVConfirmationView.as_view(),
        name="cv_confirmation",
    ),
    path(
        "cv/<uuid:cv_id>/resultats/",
        ResultatsAnalyseView.as_view(),
        name="cv_results",
    ),
    path(
        "opportunite/<int:pk>/",
        OpportuniteDetailView.as_view(),
        name="opportunite_detail",
    ),
]
