from uuid import UUID

from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers as drf_serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.mappers import (
    RecrutementKanbanMapper,
    RecrutementListeMapper,
)
from presentation.recruteur.serializers import (
    CandidatureListeSerializer,
    RecrutementDetailKanbanSerializer,
    RecrutementsFiltersSerializer,
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
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000002",
                    "date_soumission": "2025-06-11T14:30:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000002",
                        "nom": "Martin",
                        "prenom": "Bruno",
                    },
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000003",
                    "date_soumission": "2025-06-12T11:00:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000003",
                        "nom": "Leroy",
                        "prenom": "Camille",
                    },
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000004",
                    "date_soumission": "2025-06-13T08:45:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000004",
                        "nom": "Moreau",
                        "prenom": "David",
                    },
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
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000006",
                    "date_soumission": "2025-06-09T16:20:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000006",
                        "nom": "Petit",
                        "prenom": "François",
                    },
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000007",
                    "date_soumission": "2025-06-07T13:10:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000007",
                        "nom": "Roux",
                        "prenom": "Géraldine",
                    },
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
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000009",
                    "date_soumission": "2025-06-04T11:45:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000009",
                        "nom": "Michel",
                        "prenom": "Ivan",
                    },
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
                },
                {
                    "uuid": "dddddddd-0001-0001-0001-000000000011",
                    "date_soumission": "2025-06-02T10:15:00Z",
                    "candidat": {
                        "uuid": "eeeeeeee-0001-0001-0001-000000000011",
                        "nom": "Richard",
                        "prenom": "Kevin",
                    },
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
    },
)
class RecrutementKanbanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        # TODO: remplacer par get_recrutement_detail_usecase
        raw = _STATIC_RECRUTEMENTS_DETAIL_BY_ID.get(str(recrutement_uuid))
        if raw is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        detail = RecrutementKanbanMapper().from_domain(raw)
        serializer = RecrutementDetailKanbanSerializer(detail)
        return Response(serializer.data)


@extend_schema(
    summary="Détail d'un recrutement — vue liste (paginée)",
    tags=["recruteur"],
    responses={
        200: inline_serializer(
            name="PaginatedCandidatureListeResponse",
            fields={
                "count": drf_serializers.IntegerField(),
                "next": drf_serializers.CharField(allow_null=True),
                "previous": drf_serializers.CharField(allow_null=True),
                "results": CandidatureListeSerializer(many=True),
            },
        ),
        400: GenericErrorSerializer,
        401: TokenErrorSerializer,
        404: GenericErrorSerializer,
    },
)
class RecrutementListeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(
        self, request: Request, organisme_uuid: UUID, recrutement_uuid: UUID
    ) -> Response:
        filters = RecrutementsFiltersSerializer(data=request.query_params)
        if not filters.is_valid():
            return Response(filters.errors, status=status.HTTP_400_BAD_REQUEST)

        # TODO: remplacer par get_recrutement_detail_usecase
        detail = _STATIC_RECRUTEMENTS_DETAIL_BY_ID.get(str(recrutement_uuid))
        if detail is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        validated: dict = filters.validated_data  # type: ignore[assignment]
        page = validated["page"]
        size = validated["size"]

        all_candidatures = RecrutementListeMapper().from_domain(detail) or []
        count = len(all_candidatures)
        offset = (page - 1) * size
        page_data = all_candidatures[offset : offset + size]

        serializer = CandidatureListeSerializer(page_data, many=True)

        base_url = request.build_absolute_uri(request.path)

        def build_url(p: int) -> str:
            return f"{base_url}?page={p}&size={size}"

        next_url = build_url(page + 1) if page * size < count else None
        previous_url = build_url(page - 1) if page > 1 else None

        return Response(
            {
                "count": count,
                "next": next_url,
                "previous": previous_url,
                "results": serializer.data,
            }
        )
