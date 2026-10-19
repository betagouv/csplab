from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.identite.services.create_agent import create_agent
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.serializers import AgentSerializer, CreateAgentSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Créer un profil agent",
        tags=["recruteur"],
        request=CreateAgentSerializer,
        responses={
            **generic_response_format,
            201: AgentSerializer,
            400: GenericErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
        },
    ),
)
class AgentsView(SessionApiMixin, APIView):
    def post(self, request: Request) -> Response:
        serializer = CreateAgentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            profil = create_agent(**serializer.validated_data, utilisateur=request.user)
            return Response(
                AgentSerializer(profil).data, status=status.HTTP_201_CREATED
            )
        except ProfilAgentExisteDeja as e:
            return Response(
                GenericErrorSerializer({"error": str(e)}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (AccesOrganismeRefuse, OperationOrganismeRefusee) as e:
            return Response(
                GenericErrorSerializer({"error": str(e)}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        except OrganismeNexistePas:
            return Response(
                GenericErrorSerializer({"error": "organisme_id: Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                GenericErrorSerializer({"error": "Unexpected error"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
