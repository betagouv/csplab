from uuid import UUID, uuid4

from django.utils.timezone import now
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.serializers import (
    AgentOrganismeSerializer,
    SetAgentRoleOnOrganismeSerializer,
)

# TODO : données statiques en attendant le branchement sur OrganismeAgentModel
# (issue à venir)
_AGENTS_STATIQUES = [
    {
        "agent_id": uuid4(),
        "nom": "Dupont",
        "prenom": "Jeanne",
        "email": "jeanne.dupont@example.gouv.fr",
        "poste": "Responsable recrutement",
        "role": AgentOrganismeRole.RESPONSABLE.value,
        "date_derniere_activite": "2026-08-18T09:12:00Z",
        "date_creation_compte": "2025-01-10T08:00:00Z",
    },
    {
        "agent_id": uuid4(),
        "nom": "Martin",
        "prenom": "Lucas",
        "email": "lucas.martin@example.gouv.fr",
        "poste": "Chargé de recrutement",
        "role": AgentOrganismeRole.MEMBRE.value,
        "date_derniere_activite": "2026-08-15T14:30:00Z",
        "date_creation_compte": "2025-03-22T08:00:00Z",
    },
]


@extend_schema_view(
    get=extend_schema(
        summary="Liste des agents rattachés à un organisme",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: AgentOrganismeSerializer(many=True),
        },
    ),
    post=extend_schema(
        summary="Rattacher un agent à un organisme",
        tags=["recruteur"],
        request=SetAgentRoleOnOrganismeSerializer,
        responses={
            **generic_response_format,
            201: AgentOrganismeSerializer,
            400: GenericErrorSerializer,
        },
    ),
)
class OrganismeAgentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = AgentOrganismeSerializer(_AGENTS_STATIQUES, many=True)
        return Response(serializer.data)

    def post(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = SetAgentRoleOnOrganismeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        agent = {
            "agent_id": data["agent_uuid"],
            "nom": "",
            "prenom": "",
            "email": "",
            "poste": "",
            "role": data["role"],
            "date_derniere_activite": None,
            "date_creation_compte": now(),
        }
        out_serializer = AgentOrganismeSerializer(agent)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)
