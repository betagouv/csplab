from django.urls import path

from presentation.ingestion.views import (
    ArchiveOffersView,
    ConcoursUploadView,
    OffersListView,
    OffersUpsertView,
)
from presentation.ingestion.views.metiers import MetiersListView
from presentation.ingestion.views.sources import SourcesListView

app_name = "ingestion"

urlpatterns = [
    path("concours/upload/", ConcoursUploadView.as_view(), name="concours_upload"),
    path("sources/", SourcesListView.as_view(), name="sources_list"),
    path("offres/", OffersListView.as_view(), name="offers_list"),
    path("offres/archiver", ArchiveOffersView.as_view(), name="offers_archive"),
    path("offres/creer_modifier/", OffersUpsertView.as_view(), name="offers_upsert"),
    path("metiers/", MetiersListView.as_view(), name="metiers_list"),
]
