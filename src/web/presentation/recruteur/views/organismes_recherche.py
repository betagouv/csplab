from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.services.search_organismes import search_organismes
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, generic_response_format
from presentation.recruteur.serializers import (
    OrganismeRechercheSerializer,
    RechercheOrganismeQuerySerializer,
)


@extend_schema_view(
    get=extend_schema(
        summary="Rechercher des organismes par nom",
        tags=["recruteur"],
        parameters=[RechercheOrganismeQuerySerializer],
        responses={
            **generic_response_format,
            200: OrganismeRechercheSerializer(many=True),
            400: GenericErrorSerializer,
        },
    ),
)
class OrganismesRechercheView(SessionApiMixin, APIView):
    def get(self, request: Request) -> Response:
        query = RechercheOrganismeQuerySerializer(data=request.query_params)
        if not query.is_valid():
            message = next(iter(query.errors.values()))[0]
            return Response(
                GenericErrorSerializer({"error": str(message)}).data,
                status=status.HTTP_400_BAD_REQUEST,
            )

        organismes = search_organismes(
            utilisateur=request.user,
            nom=query.validated_data["nom"],
            taille=query.validated_data["taille"],
        )
        return Response(OrganismeRechercheSerializer(organismes, many=True).data)

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, OperationOrganismeRefusee):
            return Response(
                GenericErrorSerializer({"error": str(exc)}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        if isinstance(exc, exceptions.APIException):
            return super().handle_exception(exc)
        # TODO(#1618): journaliser l'erreur inattendue avant de renvoyer le 500
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
