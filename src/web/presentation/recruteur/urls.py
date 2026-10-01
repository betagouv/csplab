from django.urls import path

from presentation.recruteur.views.agent_search import AgentRechercheView
from presentation.recruteur.views.agents import AgentsView
from presentation.recruteur.views.candidature_conversation_detail import (
    CandidatureConversationDetailView,
)
from presentation.recruteur.views.candidature_conversations import (
    CandidatureConversationsView,
)
from presentation.recruteur.views.candidature_detail import CandidatureDetailView
from presentation.recruteur.views.candidature_logs import CandidatureLogsView
from presentation.recruteur.views.documents import (
    CandidatureDocumentsView,
    DocumentView,
)
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
    MotifsRefusOrganismeView,
    OrganismeDetailView,
)
from presentation.recruteur.views.organismes import (
    OrganismesView,
)
from presentation.recruteur.views.recrutement_agents import (
    RecrutementAgentsView,
    RecrutementsResponsableView,
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
        name="organisme_detail",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/parametres/etapes",
        EtapesRecrutementOrganismeView.as_view(),
        name="organisme_parametres_etapes",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/parametres/etapes/init",
        InitEtapesRecrutementOrganismeView.as_view(),
        name="organisme_parametres_etapes_init",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/parametres/agents",
        OrganismeAgentsView.as_view(),
        name="organisme_parametres_agents",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/parametres/motifs-refus",
        MotifsRefusOrganismeView.as_view(),
        name="organisme_parametres_motifs_refus",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/parametres/agents/recherche",
        AgentRechercheView.as_view(),
        name="organisme_parametres_agents_recherche",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements-actifs",
        RecrutementsActifsView.as_view(),
        name="organisme_recrutements_actifs",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements-archives",
        RecrutementsArchivesView.as_view(),
        name="organisme_recrutements_archives",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/responsable",
        RecrutementsResponsableView.as_view(),
        name="organisme_recrutements_responsable",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>",
        RecrutementDetailView.as_view(),
        name="organisme_recrutement",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/kanban",
        RecrutementKanbanView.as_view(),
        name="organisme_recrutement_kanban",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/liste",
        RecrutementListeView.as_view(),
        name="organisme_recrutement_liste",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/etape",
        RecrutementCandidaturesEtapeView.as_view(),
        name="organisme_recrutement_candidatures_etape",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/<uuid:candidature_uuid>",
        CandidatureDetailView.as_view(),
        name="organisme_recrutement_candidature_detail",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/etapes",
        RecrutementEtapeView.as_view(),
        name="organisme_recrutement_etapes",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/etapes/init",
        InitRecrutementEtapeView.as_view(),
        name="organisme_recrutement_etapes_init",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/parametres/agents",
        RecrutementAgentsView.as_view(),
        name="organisme_recrutement_parametres_agents",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/<uuid:candidature_uuid>/notes",
        CandidatureNotesView.as_view(),
        name="candidature_notes",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/<uuid:candidature_uuid>/notes/<uuid:note_uuid>",
        CandidatureNoteDetailView.as_view(),
        name="candidature_note_detail",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/<uuid:candidature_uuid>/documents",
        CandidatureDocumentsView.as_view(),
        name="organisme_recrutement_candidature_documents",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/<uuid:candidature_uuid>/documents/<uuid:document_uuid>",
        DocumentView.as_view(),
        name="organisme_recrutement_candidature_document",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/<uuid:candidature_uuid>/logs",
        CandidatureLogsView.as_view(),
        name="organisme_recrutement_candidature_logs",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/<uuid:candidature_uuid>/conversations",
        CandidatureConversationsView.as_view(),
        name="organisme_recrutement_candidature_conversations",
    ),
    path(
        "organismes/<uuid:organisme_uuid>/recrutements/<uuid:recrutement_uuid>/candidatures/<uuid:candidature_uuid>/conversations/<uuid:conversation_uuid>",
        CandidatureConversationDetailView.as_view(),
        name="organisme_recrutement_candidature_conversation_detail",
    ),
]
