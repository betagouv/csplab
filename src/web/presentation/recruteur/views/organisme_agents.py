from uuid import UUID

from django.utils.timezone import now
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.usecases.list_organisme_agents import (
    ListOrganismeAgentsQuery,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    AgentOrganismeSerializer,
    SetAgentRoleOnOrganismeSerializer,
    UpdateAgentOrganismeSerializer,
)


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
    put=extend_schema(
        summary="Modifier ou revoquer un agent d'un organisme",
        tags=["recruteur"],
        request=UpdateAgentOrganismeSerializer,
        responses={
            **generic_response_format,
            200: AgentOrganismeSerializer,
            400: GenericErrorSerializer,
        },
    ),
)
class OrganismeAgentsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            usecase = self.container.list_organisme_agents_usecase()
            agents = usecase.execute(
                ListOrganismeAgentsQuery(
                    organisme_id=organisme_uuid,
                    utilisateur=UtilisateurMapper().to_domain(request),
                )
            )
            return Response(AgentOrganismeSerializer(agents, many=True).data)
        except (AccesOrganismeRefuse, OperationOrganismeRefusee):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response(
                {"organisme_uuid": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                GenericErrorSerializer({"error": "Unexpected error"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = SetAgentRoleOnOrganismeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        agent = {
            "entity_id": data["agent_id"],
            "organisme_id": "00000000-0000-0000-0000-000000000000",
            "nom": "",
            "prenom": "",
            "email": "",
            "poste": "",
            "role": data["role"],
            "date_derniere_activite": None,
            "date_creation_compte": now(),
            "date_revocation": None,
        }
        out_serializer = AgentOrganismeSerializer(agent)
        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = UpdateAgentOrganismeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        agent = {
            "entity_id": data["agent_id"],
            "organisme_id": "00000000-0000-0000-0000-000000000000",
            "nom": data.get("nom", ""),
            "prenom": data.get("prenom", ""),
            "email": "",
            "poste": data.get("poste", ""),
            "role": data.get("role", ""),
            "date_derniere_activite": None,
            "date_creation_compte": now(),
            "date_revocation": data.get("date_revocation"),
        }
        out_serializer = AgentOrganismeSerializer(agent)
        return Response(out_serializer.data, status=status.HTTP_200_OK)
