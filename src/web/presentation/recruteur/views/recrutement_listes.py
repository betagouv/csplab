from django.db.models import QuerySet
from django.http import Http404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import exceptions, status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from application.recruteur.services.list_recrutements import (
    list_actives_recrutements,
    list_archived_recrutements,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import OrganismePermissionError
from infrastructure.django_apps.recruteur.models.recrutement import RecrutementModel
from presentation.api.authentication import SessionApiMixin
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.commons.pagination import PageNumberLimitPagination
from presentation.recruteur.serializers import (
    RecrutementsActifsSerializer,
    RecrutementsArchivesSerializer,
)


class RecrutementsListView(SessionApiMixin, ListAPIView):
    pagination_class = PageNumberLimitPagination

    def handle_exception(self, exc: Exception) -> Response:
        if isinstance(exc, OrganismePermissionError):
            return Response(
                GenericErrorSerializer({"error": "Forbidden."}).data,
                status=status.HTTP_403_FORBIDDEN,
            )
        if isinstance(exc, OrganismeNexistePas):
            return Response(
                GenericErrorSerializer({"error": "Not found."}).data,
                status=status.HTTP_404_NOT_FOUND,
            )
        if isinstance(exc, (exceptions.APIException, Http404)):
            return super().handle_exception(exc)
        return Response(
            GenericErrorSerializer({"error": "Unexpected error"}).data,
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@extend_schema_view(
    get=extend_schema(
        summary="Liste des recrutements actifs d'un organisme",
        description=("Retourne la liste paginée des recrutements d'un organisme. "),
        tags=["recruteur"],
        responses={
            200: RecrutementsActifsSerializer(many=True),
            400: GenericErrorSerializer,
            401: TokenErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
)
class RecrutementsActifsView(RecrutementsListView):
    serializer_class = RecrutementsActifsSerializer

    def get_queryset(self) -> QuerySet[RecrutementModel]:
        return list_actives_recrutements(
            organisme_id=self.kwargs["organisme_uuid"], utilisateur=self.request.user
        )


@extend_schema_view(
    get=extend_schema(
        summary="Liste des recrutements archivés d'un organisme",
        description=(
            "Retourne la liste paginée des recrutements archivés d'un organisme. "
        ),
        tags=["recruteur"],
        responses={
            200: RecrutementsArchivesSerializer(many=True),
            400: GenericErrorSerializer,
            401: TokenErrorSerializer,
            403: GenericErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
)
class RecrutementsArchivesView(RecrutementsListView):
    serializer_class = RecrutementsArchivesSerializer

    def get_queryset(self) -> QuerySet[RecrutementModel]:
        return list_archived_recrutements(
            organisme_id=self.kwargs["organisme_uuid"], utilisateur=self.request.user
        )
