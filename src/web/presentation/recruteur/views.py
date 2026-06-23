from uuid import UUID, uuid4

from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurQuery,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from domain.recruteur.errors.erreur_recrutement import ErreurRecruteur
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.serializers import (
    EtapeRecrutementSerializer,
    OrganismeSerializer,
    UpdateEtapeRecrutementSerializer,
    RecrutementActifSerializer,
    RecrutementArchiveSerializer,
    RecrutementsFiltersSerializer,
)

# ---------------------------------------------------------------------------
# Données statiques — TODO: remplacer par list_recrutements_usecase
# ---------------------------------------------------------------------------

_STATIC_RECRUTEMENTS_ACTIFS = [
    {
        "offer_id": "aaaaaaaa-0001-0001-0001-000000000001",
        "intitule": "Chargé de mission numérique",
        "reference_csp": "REF-2025-001",
        "localisation": {
            "zone_geographique": "M",
            "pays": "FRA",
            "region": "11",
            "departement": "075",
            "label": "Paris (75)",
            "latitude": 48.8566,
            "longitude": 2.3522,
        },
        "type_contrat": "TITULAIRE_CONTRACTUEL",
        "type_offre": None,
        "date_publication": "2025-06-22T10:00:00Z",
        "responsables": [{"nom": "Marie Dupont"}],
        "derniere_activite": "2025-06-23T08:00:00Z",
        "candidatures": {"total": None, "a_traiter": None, "en_cours": None},
    },
    {
        "offer_id": "aaaaaaaa-0001-0001-0001-000000000002",
        "intitule": "Responsable RH",
        "reference_csp": "REF-2025-002",
        "localisation": {
            "zone_geographique": "M",
            "pays": "FRA",
            "region": "84",
            "departement": "069",
            "label": "Lyon (69)",
            "latitude": 45.7640,
            "longitude": 4.8357,
        },
        "type_contrat": "CONTRACTUELS",
        "type_offre": None,
        "date_publication": "2025-06-22T09:00:00Z",
        "responsables": [{"nom": "Paul Bernard"}],
        "derniere_activite": "2025-06-23T07:00:00Z",
        "candidatures": {"total": None, "a_traiter": None, "en_cours": None},
    },
    {
        "offer_id": "aaaaaaaa-0001-0001-0001-000000000003",
        "intitule": "Ingénieur infrastructure cloud",
        "reference_csp": "REF-2025-003",
        "localisation": {
            "zone_geographique": "M",
            "pays": "FRA",
            "region": "93",
            "departement": "013",
            "label": "Marseille (13)",
            "latitude": 43.2965,
            "longitude": 5.3698,
        },
        "type_contrat": "TITULAIRE_CONTRACTUEL",
        "type_offre": None,
        "date_publication": "2025-06-21T14:00:00Z",
        "responsables": [{"nom": "Claire Moreau"}],
        "derniere_activite": "2025-06-22T16:00:00Z",
        "candidatures": {"total": None, "a_traiter": None, "en_cours": None},
    },
    {
        "offer_id": "aaaaaaaa-0001-0001-0001-000000000004",
        "intitule": "Juriste droit public",
        "reference_csp": "REF-2025-004",
        "localisation": {
            "zone_geographique": "M",
            "pays": "FRA",
            "region": "11",
            "departement": "092",
            "label": "Nanterre (92)",
            "latitude": 48.8924,
            "longitude": 2.2073,
        },
        "type_contrat": "TERRITORIAL",
        "type_offre": None,
        "date_publication": "2025-06-21T10:00:00Z",
        "responsables": [{"nom": "Marie Dupont"}, {"nom": "Paul Bernard"}],
        "derniere_activite": "2025-06-22T10:00:00Z",
        "candidatures": {"total": None, "a_traiter": None, "en_cours": None},
    },
    {
        "offer_id": "aaaaaaaa-0001-0001-0001-000000000005",
        "intitule": "Chargé de communication",
        "reference_csp": "REF-2025-005",
        "localisation": {
            "zone_geographique": "M",
            "pays": "FRA",
            "region": "76",
            "departement": "031",
            "label": "Toulouse (31)",
            "latitude": 43.6047,
            "longitude": 1.4442,
        },
        "type_contrat": "CONTRACTUELS",
        "type_offre": None,
        "date_publication": "2025-06-02T10:00:00Z",
        "responsables": [{"nom": "Sophie Leroy"}],
        "derniere_activite": "2025-06-20T10:00:00Z",
        "candidatures": {"total": None, "a_traiter": None, "en_cours": None},
    },
    {
        "offer_id": "aaaaaaaa-0001-0001-0001-000000000006",
        "intitule": "Analyste budgétaire",
        "reference_csp": "REF-2025-006",
        "localisation": {
            "zone_geographique": "M",
            "pays": "FRA",
            "region": "28",
            "departement": "067",
            "label": "Strasbourg (67)",
            "latitude": 48.5734,
            "longitude": 7.7521,
        },
        "type_contrat": "TITULAIRE_CONTRACTUEL",
        "type_offre": None,
        "date_publication": "2025-06-01T10:00:00Z",
        "responsables": [{"nom": "Claire Moreau"}],
        "derniere_activite": "2025-06-15T10:00:00Z",
        "candidatures": {"total": None, "a_traiter": None, "en_cours": None},
    },
]

_STATIC_RECRUTEMENTS_ARCHIVES = [
    {
        "offer_id": "bbbbbbbb-0001-0001-0001-000000000001",
        "intitule": "Directeur des systèmes d'information",
        "reference_csp": "REF-2024-A01",
        "localisation": {
            "zone_geographique": "M",
            "pays": "FRA",
            "region": "11",
            "departement": "075",
            "label": "Paris (75)",
            "latitude": 48.8566,
            "longitude": 2.3522,
        },
        "type_contrat": "TITULAIRE_CONTRACTUEL",
        "type_offre": None,
        "date_publication": "2024-12-01T10:00:00Z",
        "responsables": [{"nom": "Marie Dupont"}],
        "derniere_activite": "2025-06-23T08:00:00Z",
        "finalise": True,
        "recrute": "Sophie Leblanc",
    },
    {
        "offer_id": "bbbbbbbb-0001-0001-0001-000000000002",
        "intitule": "Chef de projet transformation numérique",
        "reference_csp": "REF-2024-A02",
        "localisation": {
            "zone_geographique": "M",
            "pays": "FRA",
            "region": "84",
            "departement": "069",
            "label": "Lyon (69)",
            "latitude": 45.7640,
            "longitude": 4.8357,
        },
        "type_contrat": "CONTRACTUELS",
        "type_offre": None,
        "date_publication": "2024-11-15T10:00:00Z",
        "responsables": [{"nom": "Paul Bernard"}],
        "derniere_activite": "2025-06-23T08:00:00Z",
        "finalise": False,
        "recrute": None,
    },
    {
        "offer_id": "bbbbbbbb-0001-0001-0001-000000000003",
        "intitule": "Conseiller en mobilité professionnelle",
        "reference_csp": "REF-2024-A03",
        "localisation": {
            "zone_geographique": "M",
            "pays": "FRA",
            "region": "93",
            "departement": "013",
            "label": "Marseille (13)",
            "latitude": 43.2965,
            "longitude": 5.3698,
        },
        "type_contrat": "TERRITORIAL",
        "type_offre": None,
        "date_publication": "2024-10-01T10:00:00Z",
        "responsables": [{"nom": "Claire Moreau"}],
        "derniere_activite": "2025-01-15T10:00:00Z",
        "finalise": True,
        "recrute": "Jean Martin",
    },
]


@extend_schema(
    summary="Detail d'un organisme",
    tags=["recruteur"],
    responses={
        200: OrganismeSerializer,
        401: TokenErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class OrganismeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganismeSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            usecase = self.container.get_organisme_recruteur_usecase()
            organisme = usecase.execute(
                GetOrganismeRecruteurQuery(organisme_id=organisme_uuid)
            )
            serializer = OrganismeSerializer(organisme)
            return Response(serializer.data)
        except ErreurRecruteur:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        summary="Liste des étapes de recrutement d'un organisme",
        tags=["recruteur"],
        responses={
            200: EtapeRecrutementSerializer(many=True),
            401: TokenErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
    put=extend_schema(
        summary="Modifier les étapes de recrutement d'un organisme",
        tags=["recruteur"],
        request=UpdateEtapeRecrutementSerializer(many=True),
        responses={
            200: EtapeRecrutementSerializer(many=True),
            400: GenericErrorSerializer,
            401: TokenErrorSerializer,
            404: GenericErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
)
class EtapesRecrutementOrganismeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            usecase = self.container.get_organisme_recruteur_usecase()
            organisme = usecase.execute(
                GetOrganismeRecruteurQuery(organisme_id=organisme_uuid)
            )
            etapes = organisme.etapes or ()
            data = [
                {
                    "etape_uuid": str(e.entity_id),
                    "nom": e.nom,
                    "categorie": e.categorie.name,
                }
                for e in etapes
            ]
            serializer = EtapeRecrutementSerializer(data, many=True)
            return Response(serializer.data)
        except ErreurRecruteur:
            return Response(
                {"organisme_uuid": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request: Request, organisme_uuid: UUID) -> Response:
        serializer = UpdateEtapeRecrutementSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # TODO: remplacer par le use case update_organisme_steps_usecase
        validated_etapes: list = serializer.validated_data  # type: ignore[assignment]
        data = [
            {
                "etape_uuid": str(etape.get("etape_uuid") or uuid4()),
                "nom": etape["nom"],
                "categorie": etape["categorie"],
            }
            for etape in validated_etapes
        ]
        out_serializer = EtapeRecrutementSerializer(data, many=True)
        return Response(out_serializer.data)


@extend_schema(
    summary="Initialiser les étapes de recrutement par défaut d'un organisme",
    tags=["recruteur"],
    request=None,
    responses={
        201: EtapeRecrutementSerializer(many=True),
        401: TokenErrorSerializer,
        404: GenericErrorSerializer,
        500: GenericErrorSerializer,
    },
)
class InitEtapesRecrutementOrganismeView(APIView):
    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.container = recruteur_container()

    def post(self, request: Request, organisme_uuid: UUID) -> Response:
        try:
            usecase = self.container.initialize_organisme_steps_usecase()
            organisme = usecase.execute(
                InitializeOrganismeStepsCommand(organisme_id=organisme_uuid)
            )
            etapes = organisme.etapes or ()
            data = [
                {
                    "etape_uuid": str(e.entity_id),
                    "nom": e.nom,
                    "categorie": e.categorie.name,
                }
                for e in etapes
            ]
            serializer = EtapeRecrutementSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ErreurRecruteur:
            return Response(
                {"organisme_uuid": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    get=extend_schema(
        summary="Liste des recrutements d'un organisme",
        description=(
            "Retourne la liste paginée des recrutements d'un organisme. "
            "Deux onglets disponibles via le paramètre `filtre` : "
            "`actifs` (recrutements en cours, défaut) et `archives` (offres archivées)."
        ),
        tags=["recruteur"],
        responses={
            200: RecrutementActifSerializer(many=True),
            400: GenericErrorSerializer,
            401: TokenErrorSerializer,
            500: GenericErrorSerializer,
        },
    ),
)
class RecrutementsOrganismeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, organisme_uuid: UUID) -> Response:
        filters = RecrutementsFiltersSerializer(data=request.query_params)
        if not filters.is_valid():
            return Response(filters.errors, status=status.HTTP_400_BAD_REQUEST)

        validated: dict = filters.validated_data  # type: ignore[assignment]
        filtre = validated["filtre"]
        page = validated["page"]
        size = validated["size"]

        # TODO: remplacer par le use case list_recrutements_usecase
        if filtre == "archives":
            dataset: list = _STATIC_RECRUTEMENTS_ARCHIVES
            serializer_class = RecrutementArchiveSerializer
        else:
            dataset = _STATIC_RECRUTEMENTS_ACTIFS
            serializer_class = RecrutementActifSerializer

        count = len(dataset)
        offset = (page - 1) * size
        page_data = dataset[offset : offset + size]

        serializer = serializer_class(page_data, many=True)

        base_url = request.build_absolute_uri(request.path)

        def build_url(p: int) -> str:
            return f"{base_url}?filtre={filtre}&page={p}&size={size}"

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
