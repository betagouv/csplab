from typing import Generic, TypeVar
from uuid import UUID

from ddd.page_interface import IPage
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.usecases.lister_mes_recrutements import (
    ListerMesRecrutementsQuery,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.commons.pagination import WebPagination
from presentation.recruteur.mappers import (
    RecrutementKanbanMapper,
    RecrutementListeMapper,
)
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


# ---------------------------------------------------------------------------
# Données statiques — TODO: remplacer par get_recrutement_detail_usecase
# ---------------------------------------------------------------------------

_STATIC_RECRUTEMENT_DETAIL = {
    "offer_id": "aaaaaaaa-0001-0001-0001-000000000001",
    "intitule": "Chargé de mission numérique",
    "date_publication": "2025-06-22T10:00:00Z",
    "localisation": {
        "zone_geographique": "EU",
        "pays": "FRA",
        "region": "11",
        "departement": "75",
        "localisation_label": "Paris 8e arrondissement",
        "latitude": 48.8748,
        "longitude": 2.3070,
    },
    "organisme_recruteur": {
        "nom": "Mairie de Paris",
        "siret": "21750001600019",
    },
    "categorie_offre": "A",
    "etapes": [
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000001",
            "nom": "Réception des candidatures",
            "categorie": "ENTREE",
            "candidatures": [
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000001",
                    "date_soumission": "2025-06-10T09:15:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000001",
                        "nom": "Dupont",
                        "prenom": "Alice",
                    },
                    "date_derniere_activite": "2025-06-11T10:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000002",
                    "date_soumission": "2025-06-11T14:30:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000002",
                        "nom": "Martin",
                        "prenom": "Bruno",
                    },
                    "date_derniere_activite": "2025-06-12T09:15:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000003",
                    "date_soumission": "2025-06-12T11:00:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000003",
                        "nom": "Leroy",
                        "prenom": "Camille",
                    },
                    "date_derniere_activite": "2025-06-12T11:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000004",
                    "date_soumission": "2025-06-13T08:45:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000004",
                        "nom": "Moreau",
                        "prenom": "David",
                    },
                    "date_derniere_activite": "2025-06-13T08:45:00Z",
                },
            ],
        },
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000002",
            "nom": "Présélection",
            "categorie": "EN_COURS",
            "candidatures": [
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000005",
                    "date_soumission": "2025-06-08T10:00:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000005",
                        "nom": "Bernard",
                        "prenom": "Élise",
                    },
                    "date_derniere_activite": "2025-06-11T10:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000006",
                    "date_soumission": "2025-06-09T16:20:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000006",
                        "nom": "Petit",
                        "prenom": "François",
                    },
                    "date_derniere_activite": "2025-06-12T09:15:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000007",
                    "date_soumission": "2025-06-07T13:10:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000007",
                        "nom": "Roux",
                        "prenom": "Géraldine",
                    },
                    "date_derniere_activite": "2025-06-12T11:00:00Z",
                },
            ],
        },
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000003",
            "nom": "Entretien",
            "categorie": "EN_COURS",
            "candidatures": [
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000008",
                    "date_soumission": "2025-06-05T09:30:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000008",
                        "nom": "Simon",
                        "prenom": "Hélène",
                    },
                    "date_derniere_activite": "2025-06-11T10:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000009",
                    "date_soumission": "2025-06-04T11:45:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000009",
                        "nom": "Michel",
                        "prenom": "Ivan",
                    },
                    "date_derniere_activite": "2025-06-13T08:45:00Z",
                },
            ],
        },
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000004",
            "nom": "Candidatures refusées",
            "categorie": "REFUS",
            "candidatures": [
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000010",
                    "date_soumission": "2025-06-03T14:00:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000010",
                        "nom": "Thomas",
                        "prenom": "Juliette",
                    },
                    "date_derniere_activite": "2025-06-11T10:00:00Z",
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000011",
                    "date_soumission": "2025-06-02T10:15:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000011",
                        "nom": "Richard",
                        "prenom": "Kevin",
                    },
                    "date_derniere_activite": "2025-06-12T09:15:00Z",
                },
            ],
        },
        {
            "etape_uuid": "cccccccc-0001-0001-0001-000000000005",
            "nom": "Candidature acceptée",
            "categorie": "ACCEPTE",
            "candidatures": [],
        },
    ],
}

# Lookup {offer_id: detail} pour simulation de la BDD
_STATIC_RECRUTEMENTS_DETAIL_BY_ID: dict = {
    _STATIC_RECRUTEMENT_DETAIL["offer_id"]: _STATIC_RECRUTEMENT_DETAIL,
}


@extend_schema(
    summary="Détail d'un recrutement — vue kanban",
    tags=["recruteur"],
    responses={
        200: RecrutementDetailKanbanSerializer,
        401: TokenErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class RecrutementKanbanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            # TODO: remplacer par get_recrutement_detail_usecase
            raw = _STATIC_RECRUTEMENTS_DETAIL_BY_ID.get(str(recrutement_uuid))
            if raw is None:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )
            detail = RecrutementKanbanMapper().from_domain(raw)
            serializer = RecrutementDetailKanbanSerializer(detail)
            return Response(serializer.data)
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
        404: GenericErrorSerializer,
    },
)
class RecrutementListeView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = WebPagination

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        try:
            # TODO: remplacer par get_recrutement_detail_usecase
            detail = _STATIC_RECRUTEMENTS_DETAIL_BY_ID.get(str(recrutement_uuid))
            if detail is None:
                return Response(
                    {"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND
                )

            all_candidatures = RecrutementListeMapper().from_domain(detail) or []
            result = ListPage(all_candidatures)

            paginator = WebPagination()
            items = paginator.paginate(result, request)
            return paginator.get_paginated_response(
                CandidatureListeSerializer(items, many=True).data
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
