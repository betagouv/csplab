from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.identite.usecases.create_agent import CreateAgentInput
from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from infrastructure.di.identite.identite_factory import create_identite_container
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
        },
    ),
)
class AgentsView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = create_identite_container()

    def post(self, request: Request) -> Response:
        serializer = CreateAgentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            usecase = self.container.create_agent_usecase()
            agent = usecase.execute(CreateAgentInput(**serializer.validated_data))
            return Response(AgentSerializer(agent).data, status=status.HTTP_201_CREATED)
        except ProfilAgentExisteDeja as e:
            return Response(
                GenericErrorSerializer({"error": str(e)}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                GenericErrorSerializer({"error": "Unexpected error"}).data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
