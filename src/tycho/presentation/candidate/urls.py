"""URL configuration for candidate app."""

from django.urls import path

from presentation.candidate.views.corps_search import CorpsSearchView
from presentation.candidate.views.cv_flow import (
    CVResultsView,
    CVUploadView,
)
from presentation.candidate.views.cv_no_results import CVNoResultsView

app_name = "candidate"

urlpatterns = [
    path("", CorpsSearchView.as_view(), name="index"),
    path("cv-upload/", CVUploadView.as_view(), name="cv_upload"),
    path(
        "cv/<uuid:cv_uuid>/results/",
        CVResultsView.as_view(),
        name="cv_results",
    ),
    path(
        "cv/<uuid:cv_uuid>/no-results/",
        CVNoResultsView.as_view(),
        name="cv_no_results",
    ),
]
