from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.usecases.lister_mes_recrutements import (
    ListerMesRecrutementsQuery,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.commons.pagination import WebPagination
from presentation.recruteur.mappers import utilisateur_from_request
from presentation.recruteur.serializers import (
    RecrutementsActifsSerializer,
    RecrutementsArchivesSerializer,
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
class RecrutementsActifsView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = WebPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            list_usecase = self.container.lister_mes_recrutements_usecase()
            result = list_usecase.execute(
                ListerMesRecrutementsQuery(
                    organisme_id=organisme_uuid,
                    statut=StatutRecrutement.ACTIF,
                    utilisateur=utilisateur_from_request(request),
                )
            )

            paginator = WebPagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                RecrutementsActifsSerializer(items, many=True).data
            )
        except AccesOrganismeRefuse:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
class RecrutementsArchivesView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = WebPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            list_usecase = self.container.lister_mes_recrutements_usecase()
            result = list_usecase.execute(
                ListerMesRecrutementsQuery(
                    organisme_id=organisme_uuid,
                    statut=StatutRecrutement.ARCHIVE,
                    utilisateur=utilisateur_from_request(request),
                )
            )

            paginator = WebPagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                RecrutementsArchivesSerializer(items, many=True).data
            )

        except AccesOrganismeRefuse:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
