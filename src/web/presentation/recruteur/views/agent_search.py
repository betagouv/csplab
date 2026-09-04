from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.search_agent_by_email import search_agent_by_email
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    AgentRechercheSerializer,
    RechercheAgentQuerySerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="Rechercher un agent par email exact",
        tags=["recruteur"],
        parameters=[RechercheAgentQuerySerializer],
        responses={
            **generic_response_format,
            200: AgentRechercheSerializer,
            400: GenericErrorSerializer,
        },
    ),
)
class AgentRechercheView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        query = RechercheAgentQuerySerializer(data=request.query_params)
        if not query.is_valid():
            message = next(iter(query.errors.values()))[0]
            return Response(
                GenericErrorSerializer({"error": str(message)}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            agent = search_agent_by_email(
                organisme_id=organisme_uuid,
                # TODO : to refactor in ADR-009 style
                utilisateur=UtilisateurMapper().to_domain(request),
                email=query.validated_data["email"],
            )
        except (AccesOrganismeRefuse, OperationOrganismeRefusee) as e:
            return Response(
                GenericErrorSerializer({"error": str(e)}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        except OrganismeNexistePas as e:
            return Response(
                GenericErrorSerializer({"error": str(e)}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception:
            return Response(
                GenericErrorSerializer({"error": "Unexpected error"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if agent is None:
            return Response(
                GenericErrorSerializer({"error": "Agent introuvable."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(AgentRechercheSerializer(agent).data)
