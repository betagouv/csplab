from django.urls import path

from presentation.ingestion.views import (
    ArchiveOffersView,
    ConcoursUploadView,
    OffersListView,
    SourcesListView,
)

app_name = "ingestion"

urlpatterns = [
    path("concours/upload/", ConcoursUploadView.as_view(), name="concours_upload"),
    path("offers/", OffersListView.as_view(), name="offers_list"),
    path("sources/", SourcesListView.as_view(), name="sources_list"),
    path(
        "offers/<str:reference>/archive",
        ArchiveOffersView.as_view(),
        name="offers_archive",
    ),
]
