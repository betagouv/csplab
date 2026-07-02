from uuid import UUID

from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers as drf_serializers
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
from application.recruteur.usecases.update_organisme_steps import (
    EtapeData,
    UpdateOrganismeStepsCommand,
)
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.erreur_recrutement import (
    ConfigurationEtapesInvalide,
    ErreurRecruteur,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.di.recruteur.recruteur_factory import recruteur_container
from presentation.api.serializers import GenericErrorSerializer, TokenErrorSerializer
from presentation.recruteur.mappers import (
    EtapesMapper,
    RecrutementKanbanMapper,
    RecrutementListeMapper,
)
from presentation.recruteur.serializers import (
    CandidatureListeSerializer,
    EtapeRecrutementSerializer,
    OrganismeSerializer,
    RecrutementActifSerializer,
    RecrutementArchiveSerializer,
    RecrutementDetailKanbanSerializer,
    RecrutementsFiltersSerializer,
    UpdateEtapeRecrutementSerializer,
)

# ---------------------------------------------------------------------------
# Données statiques — TODO: remplacer par list_recrutements_usecase
# ---------------------------------------------------------------------------

_STATIC_RECRUTEMENTS_ACTIFS = [
    {
        "offer_id": "aaaaaaaa-0001-0001-0001-000000000001",
        "intitule": "Chargé de mission numérique",
        "reference_csp": "REF-2025-001",
        "type_contrat": "TITULAIRE_CONTRACTUEL",
        "kind_contrat": None,
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
        "type_contrat": "CONTRACTUELS",
        "kind_contrat": None,
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
        "type_contrat": "TITULAIRE_CONTRACTUEL",
        "kind_contrat": None,
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
        "type_contrat": "TERRITORIAL",
        "kind_contrat": None,
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
        "type_contrat": "CONTRACTUELS",
        "kind_contrat": None,
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
        "type_contrat": "TITULAIRE_CONTRACTUEL",
        "kind_contrat": None,
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
        "type_contrat": "TITULAIRE_CONTRACTUEL",
        "kind_contrat": None,
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
        "type_contrat": "CONTRACTUELS",
        "kind_contrat": None,
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
        "type_contrat": "TERRITORIAL",
        "kind_contrat": None,
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
        except (ErreurRecruteur, OrganismeNexistePas):
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
            data = EtapesMapper().from_domain(organisme)
            serializer = EtapeRecrutementSerializer(data, many=True)
            return Response(serializer.data)
        except (ErreurRecruteur, OrganismeNexistePas):
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

        validated_etapes: list = serializer.validated_data  # type: ignore[assignment]
        etapes = [
            EtapeData(
                etape_uuid=etape.get("etape_uuid"),
                nom=etape["nom"],
                categorie=CategorieEtapeRecrutement[etape["categorie"]],
            )
            for etape in validated_etapes
        ]
        try:
            utilisateur_id = UUID(request.user.username)
            usecase = self.container.update_organisme_steps_usecase()
            organisme = usecase.execute(
                UpdateOrganismeStepsCommand(utilisateur_id, organisme_uuid, etapes)
            )
            data = EtapesMapper().from_domain(organisme)
            out_serializer = EtapeRecrutementSerializer(data, many=True)
            return Response(out_serializer.data)
        except ConfigurationEtapesInvalide as e:
            return Response({"error": e.raison}, status=status.HTTP_400_BAD_REQUEST)
        except OrganismeNexistePas:
            return Response(
                {"organisme_uuid": "Not found."}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception:
            serializer = GenericErrorSerializer({"error": "Unexpected error"})
            return Response(
                serializer.data, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
            data = EtapesMapper().from_domain(organisme)
            serializer = EtapeRecrutementSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ErreurRecruteur, OrganismeNexistePas):
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
            200: inline_serializer(
                name="PaginatedRecrutementsResponse",
                fields={
                    "count": drf_serializers.IntegerField(),
                    "next": drf_serializers.CharField(allow_null=True),
                    "previous": drf_serializers.CharField(allow_null=True),
                    "results": RecrutementActifSerializer(many=True),
                },
            ),
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

        # TODO: switch to QuerySetPage once the use case is wired up.
        # TODO: consolidate pagination logic with OffersListView
        #       (see presentation/ingestion/views.py) rather than
        # duplicating it here.
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
