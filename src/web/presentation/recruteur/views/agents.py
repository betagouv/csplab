from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.identite.usecases.create_agent import CreateAgentInput
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from infrastructure.di.identite.identite_factory import create_identite_container
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.mappers import UtilisateurMapper
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
class AgentsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_identite_container()
        self.user_mapper = UtilisateurMapper()

    def post(self, request: Request) -> Response:
        serializer = CreateAgentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            usecase = self.container.create_agent_usecase()
            agent = usecase.execute(
                CreateAgentInput(
                    **serializer.validated_data,
                    utilisateur=self.user_mapper.to_domain(request),
                )
            )
            return Response(AgentSerializer(agent).data, status=status.HTTP_201_CREATED)
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
                {"organisme_id": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            return Response(
                GenericErrorSerializer({"error": "Unexpected error"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
