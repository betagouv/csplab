from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.attach_organisme_agent import (
    attach_organisme_agent,
)
from application.recruteur.services.list_organisme_agents import list_organisme_agents
from application.recruteur.services.revoke_organisme_agent import (
    revoke_organisme_agent,
)
from application.recruteur.services.update_organisme_agent import (
    update_organisme_agent,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.agent_errors import ProfilAgentNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.organisme_agent_errors import (
    AgentDejaRattache,
    AgentNonRattache,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
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
class OrganismeAgentsView(SessionApiMixin, APIView):
    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            agents = list_organisme_agents(
                organisme_id=organisme_uuid, utilisateur=request.user
            )
            return Response(AgentOrganismeSerializer(agents, many=True).data)
        except (AccesOrganismeRefuse, OperationOrganismeRefusee):
            return Response(
                GenericErrorSerializer({"error": "Forbidden."}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        except OrganismeNexistePas:
            return Response(
                GenericErrorSerializer({"error": "organisme_uuid: Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
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
            liaison = attach_organisme_agent(
                organisme_id=organisme_uuid,
                agent_id=data["agent_id"],
                role=AgentOrganismeRole(data["role"]),
                utilisateur=request.user,
            )
            return Response(
                AgentOrganismeSerializer(liaison).data,
                status=status.HTTP_201_CREATED,
            )
        except (AccesOrganismeRefuse, OperationOrganismeRefusee):
            return Response(
                GenericErrorSerializer({"error": "Forbidden."}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        except (OrganismeNexistePas, ProfilAgentNexistePas) as error:
            field = (
                "organisme_id" if isinstance(error, OrganismeNexistePas) else "agent_id"
            )
            return Response(
                GenericErrorSerializer({"error": f"{field}: Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        except AgentDejaRattache:
            return Response(
                GenericErrorSerializer(
                    {"error": "agent_id: Agent already attached to this organisme."}
                ).data,
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
            if data.get("date_revocation"):
                liaison = revoke_organisme_agent(
                    organisme_id=organisme_uuid,
                    agent_id=data["agent_id"],
                    utilisateur=request.user,
                )
            else:
                liaison = update_organisme_agent(
                    organisme_id=organisme_uuid,
                    agent_id=data["agent_id"],
                    role=AgentOrganismeRole(data["role"]),
                    utilisateur=request.user,
                )
            return Response(AgentOrganismeSerializer(liaison).data)
        except (AccesOrganismeRefuse, OperationOrganismeRefusee):
            return Response(
                GenericErrorSerializer({"error": "Forbidden."}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        except (OrganismeNexistePas, AgentNonRattache):
            return Response(
                GenericErrorSerializer({"error": "agent_id: Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                GenericErrorSerializer({"error": "Unexpected error"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
