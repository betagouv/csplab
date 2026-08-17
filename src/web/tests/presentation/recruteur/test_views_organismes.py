from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest
from django.urls import reverse
from faker import Faker
from referentiel.value_objects.verse import Verse
from rest_framework import status

from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_errors import (
    OrganismeSiretExisteDeja,
    SiretInvalide,
)
from domain.identite.errors.organisme_permission_errors import CreationOrganismeRefusee
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.erreur_recrutement import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.recruteur.organisme_factory import (
    OrganismeRecruteurFactory,
)

fake = Faker("fr_FR")

ORGANISME_UUID = fake.uuid4()
ORGANISME_URL = reverse("recruteur:organisme")
ETAPES_URL = reverse(
    "recruteur:organisme-parametres-etapes",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
INIT_ETAPES_URL = reverse(
    "recruteur:organisme-parametres-etapes-init",
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
            "etape_uuid": str(etape.entity_id),
            "nom": etape.nom,
            "categorie": etape.categorie.name,
        }
        for etape in etapes
    ]


@pytest.fixture
def identite_container():
    with patch(
        "presentation.recruteur.views.organismes.create_identite_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


@pytest.fixture
def organisme():
    org = OrganismeFactory.create_entity()
    return {
        "nom": org.nom,
        "siret": org.siret.value,
        "gestion_ats": True,
        "gestionnaire": None,
        "date_derniere_activite": "2026-01-15T10:00:00Z",
        "date_creation": "2026-01-01T09:00:00Z",
    }


siret = fake.siret().replace(" ", "")


class TestOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ORGANISME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_create_organisme(
        self,
        organisme,
        identite_container,
        authenticated_client,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme
        identite_container.create_organisme_usecase.return_value = mock_usecase
        body = {
            "nom": organisme["nom"],
            "siret": organisme["siret"],
            "versant": fake.random_choices(
                [Verse.FPE.value, Verse.FPT.value, Verse.FPH.value]
            ),
            "gestion_ats": True,
        }
        response = authenticated_client.post(ORGANISME_URL, body)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == organisme

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeSiretExisteDeja(siret),
                status.HTTP_400_BAD_REQUEST,
                {"error": OrganismeSiretExisteDeja(siret).message},
            ),
            (
                SiretInvalide(siret),
                status.HTTP_400_BAD_REQUEST,
                {"error": SiretInvalide(siret).message},
            ),
            (
                CreationOrganismeRefusee(),
                status.HTTP_403_FORBIDDEN,
                {"error": CreationOrganismeRefusee().message},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_post_returns_error_from_usecase(
        self,
        identite_container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        identite_container.create_organisme_usecase.return_value = mock_usecase
        body = {
            "nom": fake.name(),
            "siret": siret,
            "versant": fake.random_choices(
                [Verse.FPE.value, Verse.FPT.value, Verse.FPH.value]
            ),
            "gestion_ats": fake.boolean(),
        }
        response = authenticated_client.post(ORGANISME_URL, body)

        assert response.status_code == expected_status
        assert response.json() == expected_body


@pytest.fixture
def recruteur_container():
    with patch("presentation.recruteur.views.organismes.recruteur_container") as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


class TestEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeNexistePas("not found"),
                status.HTTP_404_NOT_FOUND,
                {"organisme_uuid": "Not found."},
            ),
            (
                AccesOrganismeRefuse(UUID(fake.uuid4())),
                status.HTTP_403_FORBIDDEN,
                {"detail": "Forbidden."},
            ),
        ],
    )
    def test_get_returns_error_from_usecase(
        self,
        recruteur_container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        recruteur_container.get_organisme_recruteur_usecase.return_value = mock_usecase

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == expected_status
        assert response.json() == expected_body

    def test_authenticated_access_is_ok(
        self, recruteur_container, authenticated_client
    ):
        organisme = OrganismeRecruteurFactory.create_entity()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme
        recruteur_container.get_organisme_recruteur_usecase.return_value = mock_usecase

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == etapes_as_json(organisme.etapes or ())

    def test_forwards_est_staff_to_usecase(
        self, recruteur_container, authenticated_client, test_user
    ):
        test_user.is_staff = True
        test_user.save()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = OrganismeRecruteurFactory.create_entity()
        recruteur_container.get_organisme_recruteur_usecase.return_value = mock_usecase

        authenticated_client.get(ETAPES_URL)

        command = mock_usecase.execute.call_args.args[0]
        assert command.est_staff is True


class TestInitEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(INIT_ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                OrganismeNexistePas("not found"),
                status.HTTP_404_NOT_FOUND,
                {"organisme_uuid": "Not found."},
            ),
            (
                AccesOrganismeRefuse(UUID(fake.uuid4())),
                status.HTTP_403_FORBIDDEN,
                {"detail": "Forbidden."},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_post_returns_error_from_usecase(
        self,
        recruteur_container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        recruteur_container.initialize_organisme_steps_usecase.return_value = (
            mock_usecase
        )

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == expected_status
        assert response.json() == expected_body

    def test_authenticated_post_initialize_steps(
        self, recruteur_container, authenticated_client
    ):
        organisme = OrganismeRecruteurFactory.create_entity()
        organisme.initialiser_etapes()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme
        recruteur_container.initialize_organisme_steps_usecase.return_value = (
            mock_usecase
        )

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == etapes_as_json(organisme.etapes or ())

    def test_forwards_est_staff_to_usecase(
        self, recruteur_container, authenticated_client, test_user
    ):
        test_user.is_staff = True
        test_user.save()

        organisme = OrganismeRecruteurFactory.create_entity()
        organisme.initialiser_etapes()
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme
        recruteur_container.initialize_organisme_steps_usecase.return_value = (
            mock_usecase
        )

        authenticated_client.post(INIT_ETAPES_URL)

        command = mock_usecase.execute.call_args.args[0]
        assert command.est_staff is True


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

    def test_put_mixed_existing_and_new_etapes(
        self, recruteur_container, authenticated_client
    ):
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
        recruteur_container.update_organisme_steps_usecase.return_value = mock_usecase

        payload = [
            {
                "etape_uuid": str(existing_uuid),
                "nom": "Réception",
                "categorie": "ENTREE",
            },
            {"nom": "Nouvelle étape", "categorie": "EN_COURS"},
            {
                "etape_uuid": str(other_uuid),
                "nom": "Recrutement",
                "categorie": "ACCEPTE",
            },
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == len(payload)
        assert data[0]["etape_uuid"] == str(existing_uuid)
        assert data[1]["etape_uuid"] == str(new_uuid)
        assert data[1]["nom"] == "Nouvelle étape"

    def test_put_returns_400_on_invalid_steps(
        self, recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = ConfigurationEtapesInvalide(
            "la première étape doit être de catégorie ENTREE"
        )
        recruteur_container.update_organisme_steps_usecase.return_value = mock_usecase

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
                {"organisme_uuid": "Not found."},
            ),
            (
                AccesOrganismeRefuse(UUID(fake.uuid4())),
                status.HTTP_403_FORBIDDEN,
                {"detail": "Forbidden."},
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
        recruteur_container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        recruteur_container.update_organisme_steps_usecase.return_value = mock_usecase

        response = authenticated_client.put(
            ETAPES_URL, VALID_ETAPES_PAYLOAD, format="json"
        )

        assert response.status_code == expected_status
        assert response.json() == expected_body

    def test_forwards_est_staff_to_usecase(
        self, recruteur_container, authenticated_client, test_user
    ):
        test_user.is_staff = True
        test_user.save()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = OrganismeRecruteurFactory.create_entity()
        recruteur_container.update_organisme_steps_usecase.return_value = mock_usecase

        authenticated_client.put(ETAPES_URL, VALID_ETAPES_PAYLOAD, format="json")

        command = mock_usecase.execute.call_args.args[0]
        assert command.est_staff is True
