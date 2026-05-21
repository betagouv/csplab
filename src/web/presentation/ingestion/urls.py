from django.urls import path

from presentation.ingestion.views import (
    ArchiveOffersView,
    ConcoursUploadView,
    OffersListView,
)

app_name = "ingestion"

urlpatterns = [
    path("concours/upload/", ConcoursUploadView.as_view(), name="concours_upload"),
    path("offers/", OffersListView.as_view(), name="offers_list"),
    path("offres/archiver", ArchiveOffersView.as_view(), name="offers_archive"),
]
