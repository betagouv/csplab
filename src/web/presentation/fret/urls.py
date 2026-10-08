from django.urls import path

from presentation.fret.views import OffreDetailView, OffreListView, SourceListView

app_name = "fret"

urlpatterns = [
    path("", SourceListView.as_view(), name="sources"),
    path("source/<uuid:source_id>", OffreListView.as_view(), name="offres"),
    path(
        "source/<uuid:source_id>/offre/<uuid:offre_id>",
        OffreDetailView.as_view(),
        name="offre",
    ),
]
