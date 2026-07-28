from uuid import UUID

from drf_spectacular.utils import extend_schema
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
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import (
    OrganismePermissionError,
)
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.commons.pagination import WebPagination
from presentation.recruteur.serializers import (
    CandidatureListeSerializer,
    RecrutementDetailKanbanSerializer,
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
            result = usecase.execute(
                GetRecrutementKanbanQuery(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur_id=UUID(request.user.username),
                    est_staff=request.user.is_staff,
                )
            )
            if result is None:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )

            serializer = RecrutementDetailKanbanSerializer(result)
            return Response(serializer.data)
        except OrganismePermissionError:
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
            result = usecase.execute(
                GetRecrutementListeQuery(
                    organisme_id=organisme_uuid,
                    recrutement_id=recrutement_uuid,
                    utilisateur_id=UUID(request.user.username),
                    est_staff=request.user.is_staff,
                )
            )
            if result is None:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )

            paginator = WebPagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                CandidatureListeSerializer(items, many=True).data
            )
        except OrganismePermissionError:
            return Response({"detail": "Forbidden."}, status=status.HTTP_403_FORBIDDEN)
        except OrganismeNexistePas:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
