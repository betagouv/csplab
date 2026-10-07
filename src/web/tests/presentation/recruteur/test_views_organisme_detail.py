from datetime import datetime, timezone
from unittest.mock import MagicMock, Mock, patch
from uuid import UUID

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.enums.motif_refus import MotifRefus
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.organisme_factory import (
    OrganismeRecruteurFactory,
)
from infrastructure.repositories.commons.postgres_audit_log_repository import (
    PostgresAuditLogRepository,
)

fake = Faker("fr_FR")

NB_ETAPES_PAR_DEFAUT = 6

ORGANISME_UUID = fake.uuid4()
ORGANISME_URL = reverse(
    "recruteur:organisme_detail", kwargs={"organisme_uuid": ORGANISME_UUID}
)
ETAPES_URL = reverse(
    "recruteur:organisme_parametres_etapes",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
INIT_ETAPES_URL = reverse(
    "recruteur:organisme_parametres_etapes_init",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
MOTIFS_REFUS_URL = reverse(
    "recruteur:organisme_parametres_motifs_refus",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)

VALID_ETAPES_PAYLOAD = [
    {"nom": "Réception", "categorie": "ENTREE"},
    {"nom": "Entretien", "categorie": "EN_COURS"},
    {"nom": "Refus", "categorie": "REFUS"},
    {"nom": "Recrutement", "categorie": "ACCEPTE"},
]


def etapes_as_json(etapes: tuple[EtapeRecrutement, ...]) -> list[dict]:
    return [
        {
            "uuid": str(etape.entity_id),
            "nom": etape.nom,
            "categorie": etape.categorie.name,
        }
        for etape in etapes
    ]


def _organisme_audit_logs():
    return PostgresAuditLogRepository().get_logs_for_ressource(
        "OrganismeRecruteur", UUID(ORGANISME_UUID)
    )


@pytest.fixture
def container():
    with patch(
        "presentation.recruteur.views.organisme_detail.recruteur_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


@pytest.fixture
def identite_container():
    with patch(
        "presentation.recruteur.views.organisme_detail.create_identite_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


@pytest.fixture
def staff_client(api_client):
    staff_user = UtilisateurDjangoFactory(is_staff=True)
    api_client.force_login(staff_user)
    return api_client


class TestOrganismeDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.put(ORGANISME_URL, {}, format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_get_is_unauthorized(self, api_client):
        assert api_client.get(ORGANISME_URL).status_code == (
            status.HTTP_401_UNAUTHORIZED
        )

    def test_get_organisme(self, identite_container, authenticated_client):
        organisme = OrganismeFactory.create_entity(
            entity_id=UUID(ORGANISME_UUID),
            date_creation=datetime(2026, 1, 1, 9, 0, tzinfo=timezone.utc),
            date_derniere_activite=datetime(2026, 1, 15, 10, 0, tzinfo=timezone.utc),
        )
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme
        identite_container.get_organisme_usecase.return_value = mock_usecase

        response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["uuid"] == ORGANISME_UUID
        assert response.json()["nom"] == organisme.nom
        assert response.json()["date_creation"] == "2026-01-01T09:00:00Z"

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeNexistePas(ORGANISME_UUID),
                status.HTTP_404_NOT_FOUND,
                {"error": OrganismeNexistePas(ORGANISME_UUID).message},
            ),
            (
                AccesOrganismeRefuse(UUID(ORGANISME_UUID)),
                status.HTTP_403_FORBIDDEN,
                {"error": AccesOrganismeRefuse(UUID(ORGANISME_UUID)).message},
            ),
            (
                OperationOrganismeRefusee(),
                status.HTTP_403_FORBIDDEN,
                {"error": OperationOrganismeRefusee().message},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_get_returns_error_from_usecase(
        self,
        identite_container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        identite_container.get_organisme_usecase.return_value = mock_usecase

        response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == expected_status
        assert response.json() == expected_body

    def test_put_update_organisme(
        self,
        identite_container,
        authenticated_client,
    ):
        mock_usecase = MagicMock()
        organisme = OrganismeFactory.create_entity(entity_id=UUID(ORGANISME_UUID))
        mock_usecase.execute.return_value = organisme
        identite_container.update_organisme_usecase.return_value = mock_usecase
        body = {
            "nom": organisme.nom,
            "gestion_ats": organisme.gestion_ats,
            "versant": organisme.versant.value,
        }
        response = authenticated_client.put(ORGANISME_URL, body)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["nom"] == organisme.nom
        assert response.json()["gestion_ats"] == organisme.gestion_ats

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeNexistePas(ORGANISME_UUID),
                status.HTTP_404_NOT_FOUND,
                {"error": OrganismeNexistePas(ORGANISME_UUID).message},
            ),
            (
                OperationOrganismeRefusee(),
                status.HTTP_403_FORBIDDEN,
                {"error": OperationOrganismeRefusee().message},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_put_returns_error_from_usecase(
        self,
        identite_container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        identite_container.update_organisme_usecase.return_value = mock_usecase
        nouveau_nom = fake.name()
        body = {
            "nom": nouveau_nom,
            "gestion_ats": False,
            "versant": "FPT",
        }
        response = authenticated_client.put(ORGANISME_URL, body)

        assert response.status_code == expected_status
        assert response.json() == expected_body


class TestEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_superviseur_gets_etapes(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        organisme.etapes = [
            {
                "entity_id": "7f1d4c3a-1b2e-4c5d-8e9f-0a1b2c3d4e5f",
                "categorie": "entree",
                "nom": "Réception",
            },
            {
                "entity_id": "2a3b4c5d-6e7f-4a8b-9c0d-1e2f3a4b5c6d",
                "categorie": "accepte",
                "nom": "Recrutement",
            },
        ]
        organisme.save(update_fields=["etapes"])

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {
                "uuid": "7f1d4c3a-1b2e-4c5d-8e9f-0a1b2c3d4e5f",
                "nom": "Réception",
                "categorie": "ENTREE",
            },
            {
                "uuid": "2a3b4c5d-6e7f-4a8b-9c0d-1e2f3a4b5c6d",
                "nom": "Recrutement",
                "categorie": "ACCEPTE",
            },
        ]

    def test_membre_is_forbidden(self, authenticated_client, test_user):
        create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": "Forbidden."}

    def test_superviseur_of_another_organisme_is_forbidden(
        self, authenticated_client, test_user
    ):
        OrganismeDjangoFactory(id=UUID(ORGANISME_UUID))
        create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": "Forbidden."}

    def test_unknown_organisme_returns_404(self, staff_client):
        response = staff_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "organisme_uuid: Not found."}

    @pytest.mark.parametrize(
        "client_fixture",
        ["authenticated_client", "staff_client"],
        ids=["superviseur", "staff"],
    )
    def test_supprime_organisme_returns_404(self, request, test_user, client_fixture):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        organisme.supprime_le = datetime.now(timezone.utc)
        organisme.save(update_fields=["supprime_le"])

        response = request.getfixturevalue(client_fixture).get(ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "organisme_uuid: Not found."}


class TestInitEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(INIT_ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_superviseur_initializes_etapes(self, authenticated_client, test_user):
        create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        assert OrganismeModel.objects.get(id=UUID(ORGANISME_UUID)).etapes is None

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_201_CREATED
        persisted = OrganismeModel.objects.get(id=UUID(ORGANISME_UUID)).etapes
        expected = [
            ("Réception des candidatures", "ENTREE"),
            ("Présélection", "EN_COURS"),
            ("Entretien", "EN_COURS"),
            ("Proposition", "EN_COURS"),
            ("Refus", "REFUS"),
            ("Recrutement", "ACCEPTE"),
        ]
        assert response.json() == [
            {"uuid": etape["entity_id"], "nom": nom, "categorie": categorie}
            for etape, (nom, categorie) in zip(persisted, expected, strict=True)
        ]

    def test_staff_without_liaison_initializes_etapes(self, staff_client):
        OrganismeDjangoFactory(id=UUID(ORGANISME_UUID))

        response = staff_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_201_CREATED
        persisted = OrganismeModel.objects.get(id=UUID(ORGANISME_UUID)).etapes
        assert len(persisted) == NB_ETAPES_PAR_DEFAUT
        assert [etape["uuid"] for etape in response.json()] == [
            etape["entity_id"] for etape in persisted
        ]

    def test_superviseur_replaces_existing_etapes(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
            etapes=EtapeRecrutementFactory.create_entity_batch(),
        )
        organisme.refresh_from_db()
        anciens_ids = {etape["entity_id"] for etape in organisme.etapes}

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_201_CREATED
        organisme.refresh_from_db()
        assert anciens_ids.isdisjoint(e["entity_id"] for e in organisme.etapes)

    def test_initialization_is_audited(self, authenticated_client, test_user):
        create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )

        authenticated_client.post(INIT_ETAPES_URL)

        logs = _organisme_audit_logs()
        assert len(logs) == 1
        assert logs[0].event_name == "OrganismeEtapesInitialises"
        assert logs[0].utilisateur_id == test_user.username
        assert logs[0].ressource_id == UUID(ORGANISME_UUID)

    def test_updated_at_advances(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        updated_at_avant = organisme.updated_at

        authenticated_client.post(INIT_ETAPES_URL)

        organisme.refresh_from_db()
        assert organisme.updated_at > updated_at_avant

    def test_membre_is_forbidden(self, authenticated_client, test_user):
        create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": "Forbidden."}
        assert OrganismeModel.objects.get(id=UUID(ORGANISME_UUID)).etapes is None
        assert _organisme_audit_logs() == []

    def test_superviseur_of_another_organisme_is_forbidden(
        self, authenticated_client, test_user
    ):
        OrganismeDjangoFactory(id=UUID(ORGANISME_UUID))
        create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": "Forbidden."}
        assert OrganismeModel.objects.get(id=UUID(ORGANISME_UUID)).etapes is None
        assert _organisme_audit_logs() == []

    def test_unknown_organisme_returns_404(self, staff_client):
        response = staff_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "organisme_uuid: Not found."}

    def test_supprime_organisme_returns_404(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )
        organisme.supprime_le = datetime.now(timezone.utc)
        organisme.save(update_fields=["supprime_le"])

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "organisme_uuid: Not found."}
        assert OrganismeModel.objects.get(id=UUID(ORGANISME_UUID)).etapes is None
        assert _organisme_audit_logs() == []

    @patch.object(
        AuditLogWriter,
        "log_action",
        new=Mock(side_effect=RuntimeError("audit log write failed")),
    )
    def test_audit_failure_returns_500(self, authenticated_client, test_user):
        create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestPutEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.put(ETAPES_URL, [], format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_body_returns_400(self, authenticated_client):
        response = authenticated_client.put(
            ETAPES_URL,
            [{"nom": "Entretien", "categorie": "INVALIDE"}],
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_nom_returns_400(self, authenticated_client):
        response = authenticated_client.put(
            ETAPES_URL,
            [{"categorie": "EN_COURS"}],
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_put_mixed_existing_and_new_etapes(self, container, authenticated_client):
        existing_uuid = fake.uuid4()
        new_uuid = fake.uuid4()
        other_uuid = fake.uuid4()

        organisme = OrganismeRecruteurFactory.create_entity()
        organisme._etapes = (
            EtapeRecrutement.build(
                entity_id=UUID(existing_uuid),
                nom="Réception",
                categorie=CategorieEtapeRecrutement.ENTREE,
            ),
            EtapeRecrutement.build(
                entity_id=UUID(new_uuid),
                nom="Nouvelle étape",
                categorie=CategorieEtapeRecrutement.EN_COURS,
            ),
            EtapeRecrutement.build(
                entity_id=UUID(other_uuid),
                nom="Recrutement",
                categorie=CategorieEtapeRecrutement.ACCEPTE,
            ),
        )

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme
        container.update_organisme_steps_usecase.return_value = mock_usecase

        payload = [
            {
                "uuid": str(existing_uuid),
                "nom": "Réception",
                "categorie": "ENTREE",
            },
            {"nom": "Nouvelle étape", "categorie": "EN_COURS"},
            {
                "uuid": str(other_uuid),
                "nom": "Recrutement",
                "categorie": "ACCEPTE",
            },
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == len(payload)
        assert data[0]["uuid"] == str(existing_uuid)
        assert data[1]["uuid"] == str(new_uuid)
        assert data[1]["nom"] == "Nouvelle étape"
        (command,), _ = mock_usecase.execute.call_args
        assert [e.etape_uuid for e in command.etapes] == [
            UUID(existing_uuid),
            None,
            UUID(other_uuid),
        ]

    def test_put_returns_400_on_invalid_steps(self, container, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = ConfigurationEtapesInvalide(
            "la première étape doit être de catégorie ENTREE"
        )
        container.update_organisme_steps_usecase.return_value = mock_usecase

        payload = [
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {
            "error": "la première étape doit être de catégorie ENTREE"
        }

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeNexistePas("not found"),
                status.HTTP_404_NOT_FOUND,
                {"error": "organisme_uuid: Not found."},
            ),
            (
                AccesOrganismeRefuse(UUID(fake.uuid4())),
                status.HTTP_403_FORBIDDEN,
                {"error": "Forbidden."},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_put_returns_error_from_usecase(
        self,
        container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        container.update_organisme_steps_usecase.return_value = mock_usecase

        response = authenticated_client.put(
            ETAPES_URL, VALID_ETAPES_PAYLOAD, format="json"
        )

        assert response.status_code == expected_status
        assert response.json() == expected_body

    def test_forwards_est_staff_to_usecase(
        self, container, authenticated_client, test_user
    ):
        test_user.is_staff = True
        test_user.save()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = OrganismeRecruteurFactory.create_entity()
        container.update_organisme_steps_usecase.return_value = mock_usecase

        authenticated_client.put(ETAPES_URL, VALID_ETAPES_PAYLOAD, format="json")

        command = mock_usecase.execute.call_args.args[0]
        assert command.utilisateur.is_staff is True


class TestOrganismeDetailViewDbVerified:
    def test_get_returns_persisted_organisme(self, staff_client):
        organisme = OrganismeDjangoFactory(id=UUID(ORGANISME_UUID), gestion_ats=True)

        response = staff_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["uuid"] == ORGANISME_UUID
        assert data["nom"] == organisme.nom
        assert data["versant"] == organisme.versant
        assert data["siret"] == organisme.siret
        assert data["gestion_ats"] == organisme.gestion_ats

    def test_put_updates_and_persists_the_organisme(self, staff_client):
        OrganismeDjangoFactory(id=UUID(ORGANISME_UUID), gestion_ats=False)
        nouveau_nom = fake.name()
        body = {"nom": nouveau_nom, "gestion_ats": True, "versant": "FPT"}

        response = staff_client.put(ORGANISME_URL, body)

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["nom"] == nouveau_nom
        assert response.json()["gestion_ats"] is True

        organisme = OrganismeModel.objects.get(id=UUID(ORGANISME_UUID))
        assert organisme.nom == nouveau_nom
        assert organisme.gestion_ats is True
        assert organisme.versant == "FPT"

    @pytest.mark.parametrize(
        "client_fixture",
        ["authenticated_client", "staff_client"],
        ids=["non_staff", "staff"],
    )
    def test_put_supprime_organisme_returns_404(self, request, client_fixture):
        client = request.getfixturevalue(client_fixture)
        organisme = OrganismeDjangoFactory(
            id=UUID(ORGANISME_UUID), supprime_le=datetime.now(timezone.utc)
        )
        body = {"nom": fake.name(), "gestion_ats": True, "versant": "FPT"}

        response = client.put(ORGANISME_URL, body)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": f"Organisme introuvable : {ORGANISME_UUID}"}
        assert OrganismeModel.objects.get(id=UUID(ORGANISME_UUID)).nom == organisme.nom


class TestEtapesRecrutementOrganismeViewDbVerified:
    def test_staff_without_liaison_gets_empty_list_when_etapes_is_null(
        self, staff_client
    ):
        OrganismeDjangoFactory(id=UUID(ORGANISME_UUID))
        assert OrganismeModel.objects.get(id=UUID(ORGANISME_UUID)).etapes is None

        response = staff_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_put_persists_the_etapes(self, staff_client):
        OrganismeDjangoFactory(id=UUID(ORGANISME_UUID))

        response = staff_client.put(ETAPES_URL, VALID_ETAPES_PAYLOAD, format="json")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert [{"nom": e["nom"], "categorie": e["categorie"]} for e in data] == [
            {"nom": e["nom"], "categorie": e["categorie"]} for e in VALID_ETAPES_PAYLOAD
        ]

        organisme = OrganismeModel.objects.get(id=UUID(ORGANISME_UUID))
        assert [e["nom"] for e in organisme.etapes] == [
            e["nom"] for e in VALID_ETAPES_PAYLOAD
        ]


class TestMotifsRefusOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(MOTIFS_REFUS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_non_agent_is_forbidden(self, authenticated_client):
        OrganismeDjangoFactory(id=UUID(ORGANISME_UUID))

        response = authenticated_client.get(MOTIFS_REFUS_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_unknown_organisme_returns_404(self, staff_client):
        response = staff_client.get(MOTIFS_REFUS_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_agent_gets_full_motifs_list(self, authenticated_client, test_user):
        create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT,
            utilisateur=test_user,
            id=UUID(ORGANISME_UUID),
        )

        response = authenticated_client.get(MOTIFS_REFUS_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == [
            {"value": motif.value, "label": motif.label} for motif in MotifRefus
        ]

    def test_staff_without_role_is_allowed(self, staff_client):
        OrganismeDjangoFactory(id=UUID(ORGANISME_UUID))

        response = staff_client.get(MOTIFS_REFUS_URL)

        assert response.status_code == status.HTTP_200_OK
