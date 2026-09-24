from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from application.recruteur.services.list_conversations import (
    ConversationStub,
    list_conversations,
)
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
from presentation.recruteur.serializers import ConversationSerializer


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
)
class CandidatureConversationsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    pagination_class = ConversationPagination

    def get_queryset(self) -> list[ConversationStub]:
        return list_conversations(
            organisme_id=self.kwargs["organisme_uuid"],
            recrutement_id=self.kwargs["recrutement_uuid"],
            candidature_id=self.kwargs["candidature_uuid"],
            utilisateur=UtilisateurMapper().to_domain(self.request),
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
