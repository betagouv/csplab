from uuid import UUID, uuid4

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from presentation.api.serializers import generic_response_format
from presentation.recruteur.serializers import AgentOrganismeSerializer

# TODO : données statiques en attendant le branchement sur OrganismeAgentModel
# (issue à venir)
_AGENTS_STATIQUES = [
    {
        "agent_id": uuid4(),
        "nom": "Dupont",
        "prenom": "Jeanne",
        "email": "jeanne.dupont@example.gouv.fr",
        "poste": "Responsable recrutement",
        "role": "RESPONSABLE",
        "date_derniere_activite": "2026-08-18T09:12:00Z",
        "date_creation_compte": "2025-01-10T08:00:00Z",
    },
    {
        "agent_id": uuid4(),
        "nom": "Martin",
        "prenom": "Lucas",
        "email": "lucas.martin@example.gouv.fr",
        "poste": "Chargé de recrutement",
        "role": "MEMBRE",
        "date_derniere_activite": "2026-08-15T14:30:00Z",
        "date_creation_compte": "2025-03-22T08:00:00Z",
    },
]


@extend_schema(
    summary="Liste des agents rattachés à un organisme",
    tags=["recruteur"],
    responses={
        **generic_response_format,
        200: AgentOrganismeSerializer(many=True),
    },
)
class OrganismeAgentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = AgentOrganismeSerializer(_AGENTS_STATIQUES, many=True)
        return Response(serializer.data)
