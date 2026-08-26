from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.usecases.attach_organisme_agent import (
    AttachOrganismeAgentCommand,
)
from application.recruteur.usecases.list_organisme_agents import (
    ListOrganismeAgentsQuery,
)
from application.recruteur.usecases.update_organisme_agent import (
    UpdateOrganismeAgentCommand,
)
from application.recruteur.usecases.list_organisme_agents import (
    ListOrganismeAgentsQuery,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.organisme_agent_errors import (
    AgentDejaRattache,
    AgentNonRattache,
)
from domain.recruteur.errors.organisme_agent_errors import AgentDejaRattache
from domain.recruteur.value_objects.roles import AgentOrganismeRole
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
            409: GenericErrorSerializer,
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
        try:
            usecase = self.container.attach_organisme_agent_usecase()
            agent_organisme = usecase.execute(
                AttachOrganismeAgentCommand(
                    organisme_id=organisme_uuid,
                    agent_id=data["agent_id"],
                    role=AgentOrganismeRole(data["role"]),
                    utilisateur=UtilisateurMapper().to_domain(request),
                )
            )
            return Response(
                AgentOrganismeSerializer(agent_organisme).data,
                status=status.HTTP_201_CREATED,
            )
        except (AccesOrganismeRefuse, OperationOrganismeRefusee):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response(
                {"organisme_id": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except AgentDejaRattache:
            return Response(
                {"agent_id": "Agent already attached to this organisme."},
                status=status.HTTP_409_CONFLICT,
            )
        except Exception:
            return Response(
                GenericErrorSerializer({"error": "Unexpected error"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def put(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = UpdateAgentOrganismeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        try:
            usecase = self.container.update_organisme_agent_usecase()
            agent_organisme = usecase.execute(
                UpdateOrganismeAgentCommand(
                    organisme_id=organisme_uuid,
                    agent_id=data["agent_id"],
                    role=AgentOrganismeRole(data["role"]),
                    utilisateur=UtilisateurMapper().to_domain(request),
                )
            )
            return Response(AgentOrganismeSerializer(agent_organisme).data)
        except (AccesOrganismeRefuse, OperationOrganismeRefusee):
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except (OrganismeNexistePas, AgentNonRattache):
            return Response(
                {"agent_id": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                GenericErrorSerializer({"error": "Unexpected error"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
