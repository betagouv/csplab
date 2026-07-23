from typing import Generic, TypeVar
from uuid import UUID

from ddd.page_interface import IPage
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.usecases.get_recrutement_kanban import (
    GetRecrutementKanbanQuery,
)
from application.recruteur.usecases.get_recrutement_liste import (
    GetRecrutementListeQuery,
)
from application.recruteur.usecases.lister_mes_recrutements import (
    ListerMesRecrutementsQuery,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.commons.pagination import WebPagination
from presentation.recruteur.mappers import RecrutementKanbanMapper
from presentation.recruteur.serializers import (
    CandidatureListeSerializer,
    RecrutementDetailKanbanSerializer,
    RecrutementsActifsSerializer,
    RecrutementsArchivesSerializer,
)

# ---------------------------------------------------------------------------
# Données statiques — TODO: remplacer par list_recrutements_usecase
# ---------------------------------------------------------------------------

T = TypeVar("T")


class ListPage(IPage[T], Generic[T]):
    def __init__(self, items: list[T]):
        self._items = items

    def count(self) -> int:
        return len(self._items)

    def slice(self, offset: int, limit: int):
        return iter(self._items[offset : offset + limit])


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
                    utilisateur_id=UUID(request.user.username),
                    est_staff=request.user.is_staff,
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
                    utilisateur_id=UUID(request.user.username),
                    est_staff=request.user.is_staff,
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


@extend_schema(
    summary="Détail d'un recrutement — vue kanban",
    tags=["recruteur"],
    responses={
        200: RecrutementDetailKanbanSerializer,
        401: TokenErrorSerializer,
        403: GenericErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class RecrutementKanbanView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            usecase = self.container.get_recrutement_kanban_usecase()
            raw = usecase.execute(
                GetRecrutementKanbanQuery(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur_id=UUID(request.user.username),
                    est_staff=request.user.is_staff,
                )
            )
            if raw is None:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )
            detail = RecrutementKanbanMapper().from_domain(raw)
            serializer = RecrutementDetailKanbanSerializer(detail)
            return Response(serializer.data)
        except AccesOrganismeRefuse:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema(
    summary="Détail d'un recrutement — vue liste (paginée)",
    tags=["recruteur"],
    responses={
        200: CandidatureListeSerializer(many=True),
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        403: GenericErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class RecrutementListeView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = WebPagination

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            usecase = self.container.get_recrutement_liste_usecase()
            candidatures = usecase.execute(
                GetRecrutementListeQuery(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur_id=UUID(request.user.username),
                    est_staff=request.user.is_staff,
                )
            )
            if candidatures is None:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )

            result = ListPage(candidatures)

            paginator = WebPagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                CandidatureListeSerializer(items, many=True).data
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
