from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from application.recruteur.services.conversation_stubs import ConversationStub
from application.recruteur.services.create_conversation import create_conversation
from application.recruteur.services.list_conversations import list_conversations
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.commons.pagination import PageNumberLimitPagination
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    ConversationSerializer,
    CreateConversationSerializer,
)


class ConversationPagination(PageNumberLimitPagination):
    page_size = 20


@extend_schema_view(
    get=extend_schema(
        summary="Liste des conversations d'une candidature (stub)",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: ConversationSerializer(many=True),
        },
    ),
    post=extend_schema(
        summary="Créer une conversation sur une candidature (stub)",
        tags=["recruteur"],
        request={"multipart/form-data": CreateConversationSerializer},
        responses={
            **generic_response_format,
            201: ConversationSerializer,
            400: GenericErrorSerializer,
        },
    ),
)
class CandidatureConversationsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    pagination_class = ConversationPagination
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self) -> list[ConversationStub]:
        return list_conversations(
            organisme_id=self.kwargs["organisme_uuid"],
            recrutement_id=self.kwargs["recrutement_uuid"],
            candidature_id=self.kwargs["candidature_uuid"],
            utilisateur=UtilisateurMapper().to_domain(self.request),
        )

    def post(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
    ) -> Response:
        serializer = CreateConversationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        conversation = create_conversation(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            objet=serializer.validated_data["objet"],
            content=serializer.validated_data["content"],
            documents=serializer.validated_data["documents"],
            utilisateur=UtilisateurMapper().to_domain(request),
        )
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED,
        )

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(
            exc,
            (
                AccesOrganismeRefuse,
                AccesRecrutementRefuse,
                OperationOrganismeRefusee,
                OrganismeNexistePas,
                AccesRecrutementInconnu,
                RecrutementInexistant,
                RecrutementCandidatureInexistante,
            ),
        ):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
