from django.urls import path

from presentation.recruteur.views.agents import AgentsView
from presentation.recruteur.views.notes import (
    CandidatureNoteDetailView,
    CandidatureNotesView,
)
from presentation.recruteur.views.organisme_agents import (
    OrganismeAgentsView,
)
from presentation.recruteur.views.organisme_detail import (
    EtapesRecrutementOrganismeView,
    InitEtapesRecrutementOrganismeView,
    OrganismeDetailView,
)
from presentation.recruteur.views.organismes import (
    OrganismesView,
)
from presentation.recruteur.views.recrutement_detail import (
    RecrutementCandidaturesEtapeView,
    RecrutementDetailView,
    RecrutementKanbanView,
    RecrutementListeView,
)
from presentation.recruteur.views.recrutement_listes import (
    RecrutementsActifsView,
    RecrutementsArchivesView,
)
from presentation.recruteur.views.recrutement_params import (
    InitRecrutementEtapeView,
    RecrutementEtapeView,
)

app_name = "recruteur"

urlpatterns = [
    path(
        "agents",
        AgentsView.as_view(),
        name="agents",
    ),
    path(
        "organismes",
        OrganismesView.as_view(),
        name="organismes",
    ),
    path(
        "organismes/<uuid:organisme_uuid>",
        OrganismeDetailView.as_view(),
        name="organisme-detail",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/parametres/etapes",
        EtapesRecrutementOrganismeView.as_view(),
        name="organisme-parametres-etapes",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/parametres/etapes/init",
        InitEtapesRecrutementOrganismeView.as_view(),
        name="organisme-parametres-etapes-init",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/parametres/agents",
        OrganismeAgentsView.as_view(),
        name="organisme-parametres-agents",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements-actifs",
        RecrutementsActifsView.as_view(),
        name="organisme-recrutements-actifs",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements-archives",
        RecrutementsArchivesView.as_view(),
        name="organisme-recrutements-archives",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>",
        RecrutementDetailView.as_view(),
        name="organisme-recrutement",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/kanban",
        RecrutementKanbanView.as_view(),
        name="organisme-recrutement-kanban",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/liste",
        RecrutementListeView.as_view(),
        name="organisme-recrutement-liste",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/etape",
        RecrutementCandidaturesEtapeView.as_view(),
        name="organisme-recrutement-candidatures-etape",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/etapes",
        RecrutementEtapeView.as_view(),
        name="organisme-recrutement-etapes",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/etapes/init",
        InitRecrutementEtapeView.as_view(),
        name="organisme-recrutement-etapes-init",
    ),
    path(
        "candidatures/<uuid:candidature_uuid>/notes",
        CandidatureNotesView.as_view(),
        name="candidature-notes",
    ),
    path(
        "candidatures/<uuid:candidature_uuid>/notes/<uuid:note_uuid>",
        CandidatureNoteDetailView.as_view(),
        name="candidature-note-detail",
    ),
]
