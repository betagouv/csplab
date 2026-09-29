from uuid import UUID

from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from application.recruteur.services.read_conversation import (
    MessageStub,
    read_conversation,
)
from application.recruteur.services.reply_conversation import reply_conversation
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.commons.pagination import PageNumberLimitPagination
from presentation.recruteur.mappers import UtilisateurMapper
from presentation.recruteur.serializers import (
    ConversationMessageSerializer,
    CreateMessageSerializer,
)


class MessagePagination(PageNumberLimitPagination):
    page_size = 20


@extend_schema_view(
    get=extend_schema(
        operation_id="recruteur_organismes_recrutements_candidatures_conversations_messages_list",
        summary="Messages d'une conversation d'une candidature (stub)",
        tags=["recruteur"],
        responses={
            **generic_response_format,
            200: ConversationMessageSerializer(many=True),
        },
    ),
    post=extend_schema(
        operation_id="recruteur_organismes_recrutements_candidatures_conversations_messages_create",
        summary="Répondre dans une conversation d'une candidature (stub)",
        tags=["recruteur"],
        request={"multipart/form-data": CreateMessageSerializer},
        responses={
            **generic_response_format,
            201: ConversationMessageSerializer,
            400: GenericErrorSerializer,
        },
    ),
)
class CandidatureConversationDetailView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationMessageSerializer
    pagination_class = MessagePagination
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self) -> list[MessageStub]:
        return read_conversation(
            organisme_id=self.kwargs["organisme_uuid"],
            recrutement_id=self.kwargs["recrutement_uuid"],
            candidature_id=self.kwargs["candidature_uuid"],
            conversation_id=self.kwargs["conversation_uuid"],
            utilisateur=UtilisateurMapper().to_domain(self.request),
        )

    def post(
        self,
        request: Request,
        organisme_uuid: UUID,
        recrutement_uuid: UUID,
        candidature_uuid: UUID,
        conversation_uuid: UUID,
    ) -> Response:
        serializer = CreateMessageSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        message = reply_conversation(
            organisme_id=organisme_uuid,
            recrutement_id=recrutement_uuid,
            candidature_id=candidature_uuid,
            conversation_id=conversation_uuid,
            content=serializer.validated_data["content"],
            documents=serializer.validated_data["documents"],
            utilisateur=UtilisateurMapper().to_domain(request),
        )
        return Response(
            ConversationMessageSerializer(message).data,
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
                ConversationInexistante,
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
