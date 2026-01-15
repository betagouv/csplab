"""URL configuration for candidate app."""

from django.urls import path

from presentation.candidate.views.corps_search import CorpsSearchView
from presentation.candidate.views.cv_flow import CVUploadView

app_name = "candidate"

urlpatterns = [
    path("", CorpsSearchView.as_view(), name="index"),
    path("cv-upload/", CVUploadView.as_view(), name="cv_upload"),
]
