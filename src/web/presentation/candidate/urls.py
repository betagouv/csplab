from django.urls import path

from presentation.candidate.views.cv_flow import (
    ConcoursDrawerView,
    CVResultsView,
    CVUploadView,
    OfferDrawerView,
)

app_name = "candidate"

urlpatterns = [
    path("cv-upload/", CVUploadView.as_view(), name="cv_upload"),
    path(
        "cv/<uuid:cv_uuid>/results/",
        CVResultsView.as_view(),
        name="cv_results",
    ),
    path(
        "cv/<uuid:cv_uuid>/offers/<uuid:offer_id>/detail/",
        OfferDrawerView.as_view(),
        name="offer_drawer",
    ),
    path(
        "cv/<uuid:cv_uuid>/concours/<uuid:concours_id>/detail/",
        ConcoursDrawerView.as_view(),
        name="concours_drawer",
    ),
]
