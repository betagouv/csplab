from django.urls import path

from presentation.ingestion.views.concours import ConcoursUploadView
from presentation.ingestion.views.metiers import MetiersListView
from presentation.ingestion.views.offers import (
    ArchiveOffersView,
    OffersBySourceView,
    OffersListView,
    OffersUpsertView,
)
from presentation.ingestion.views.organismes import (
    OrganismesSupprimerView,
    OrganismesUpsertView,
)
from presentation.ingestion.views.sources import SourcesListView
from presentation.ingestion.views.talentsoft_organismes import (
    TalentsoftOrganismesUpsertView,
)

app_name = "ingestion"

urlpatterns = [
    path("concours/upload", ConcoursUploadView.as_view(), name="concours_upload"),
    path("sources", SourcesListView.as_view(), name="sources_list"),
    path("offres", OffersListView.as_view(), name="offers_list"),
    path(
        "offres/sources/<uuid:source_id>",
        OffersBySourceView.as_view(),
        name="offers_by_source",
    ),
    path("offres/archiver", ArchiveOffersView.as_view(), name="offers_archive"),
    path("offres/creer_modifier", OffersUpsertView.as_view(), name="offers_upsert"),
    path(
        "organismes/creer_modifier",
        OrganismesUpsertView.as_view(),
        name="organismes_upsert",
    ),
    path(
        "organismes",
        OrganismesSupprimerView.as_view(),
        name="organismes_delete",
    ),
    path("metiers", MetiersListView.as_view(), name="metiers_list"),
    path(
        "talentsoft_organisme/creer_modifier",
        TalentsoftOrganismesUpsertView.as_view(),
        name="talentsoft_organismes_upsert",
    ),
]
