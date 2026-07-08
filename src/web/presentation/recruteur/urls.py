from django.urls import path

from presentation.recruteur.views.notes import (
    CandidatureNoteDetailView,
    CandidatureNotesView,
)
from presentation.recruteur.views.organismes import (
    EtapesRecrutementOrganismeView,
    InitEtapesRecrutementOrganismeView,
    OrganismeView,
)
from presentation.recruteur.views.recrutements import (
    RecrutementKanbanView,
    RecrutementListeView,
    RecrutementsActifsView,
    RecrutementsArchivesView,
)

app_name = "recruteur"

urlpatterns = [
    path(
        "organisme/<uuid:organisme_uuid>",
        OrganismeView.as_view(),
        name="organisme",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/parametres/etapes",
        EtapesRecrutementOrganismeView.as_view(),
        name="organisme-parametres-etapes",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/parametres/etapes/init",
        InitEtapesRecrutementOrganismeView.as_view(),
        name="organisme-parametres-etapes-init",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/recrutements-actifs",
        RecrutementsActifsView.as_view(),
        name="organisme-recrutements-actifs",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/recrutements-archives",
        RecrutementsArchivesView.as_view(),
        name="organisme-recrutements-archives",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/kanban",
        RecrutementKanbanView.as_view(),
        name="organisme-recrutement-kanban",
    ),
    path(
        "organisme/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/liste",
        RecrutementListeView.as_view(),
        name="organisme-recrutement-liste",
    ),
    path(
        "candidature/<uuid:candidature_uuid>/notes",
        CandidatureNotesView.as_view(),
        name="candidature-notes",
    ),
    path(
        # TODO supprimer candidature_id
        "candidature/<uuid:candidature_uuid>/notes/<uuid:note_uuid>",
        CandidatureNoteDetailView.as_view(),
        name="candidature-note-detail",
    ),
]
