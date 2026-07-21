from unittest.mock import MagicMock, patch
from uuid import UUID

from django.urls import reverse
from faker import Faker
from rest_framework import status

from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.erreur_recrutement import (
    ConfigurationEtapesInvalide,
    ErreurRecruteur,
)
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.factories.recruteur.organisme_factory import (
    OrganismeRecruteurFactory,
)

fake = Faker()

ORGANISME_UUID = fake.uuid4()
ORGANISME_URL = reverse(
    "recruteur:organisme", kwargs={"organisme_uuid": ORGANISME_UUID}
)
ETAPES_URL = reverse(
    "recruteur:organisme-parametres-etapes",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
INIT_ETAPES_URL = reverse(
    "recruteur:organisme-parametres-etapes-init",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)


class TestOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ORGANISME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_authenticated_access_is_ok(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_organisme = MagicMock()
        mock_organisme.nom = "COMMUNE DE BRIANCON"
        mock_organisme.siret = "21050023700354"

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = mock_organisme

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "nom": "COMMUNE DE BRIANCON",
            "siret": "21050023700354",
        }

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_returns_404_when_organisme_not_found(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = ErreurRecruteur("not found")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_returns_403_when_not_responsable(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = AccesOrganismeRefuse(UUID(fake.uuid4()))

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_forwards_est_staff_to_usecase(
        self, mock_recruteur_container, authenticated_client, test_user
    ):
        test_user.is_staff = True
        test_user.save()

        mock_organisme = MagicMock()
        mock_organisme.nom = "COMMUNE DE BRIANCON"
        mock_organisme.siret = "21050023700354"
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = mock_organisme

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        authenticated_client.get(ORGANISME_URL)

        command = mock_usecase.execute.call_args.args[0]
        assert command.est_staff is True


class TestEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_returns_404_when_organisme_not_found(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"organisme_uuid": "Not found."}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_returns_403_when_not_responsable(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = AccesOrganismeRefuse(UUID(fake.uuid4()))

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_authenticated_access_is_ok(
        self, mock_recruteur_container, authenticated_client
    ):
        organisme = OrganismeRecruteurFactory.create_entity()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_200_OK
        steps = []
        if organisme.etapes:
            steps = [
                {
                    "etape_uuid": str(etape.entity_id),
                    "nom": etape.nom,
                    "categorie": etape.categorie.name,
                }
                for etape in organisme.etapes
            ]

        assert response.json() == steps

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_forwards_est_staff_to_usecase(
        self, mock_recruteur_container, authenticated_client, test_user
    ):
        test_user.is_staff = True
        test_user.save()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = OrganismeRecruteurFactory.create_entity()

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        authenticated_client.get(ETAPES_URL)

        command = mock_usecase.execute.call_args.args[0]
        assert command.est_staff is True


class TestInitEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(INIT_ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_returns_404_when_organisme_not_found(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"organisme_uuid": "Not found."}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_returns_500_on_unexpected_error(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = Exception("unexpected")

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_returns_403_when_not_responsable(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = AccesOrganismeRefuse(UUID(fake.uuid4()))

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_authenticated_post_initialize_steps(
        self, mock_recruteur_container, authenticated_client
    ):
        organisme = OrganismeRecruteurFactory.create_entity()
        organisme.initialiser_etapes()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == [
            {
                "etape_uuid": str(etape.entity_id),
                "nom": etape.nom,
                "categorie": etape.categorie.name,
            }
            for etape in (organisme.etapes or ())
        ]

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_forwards_est_staff_to_usecase(
        self, mock_recruteur_container, authenticated_client, test_user
    ):
        test_user.is_staff = True
        test_user.save()

        organisme = OrganismeRecruteurFactory.create_entity()
        organisme.initialiser_etapes()
        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

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

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_put_mixed_existing_and_new_etapes(
        self, mock_recruteur_container, authenticated_client
    ):
        existing_uuid = fake.uuid4()
        new_uuid = fake.uuid4()
        other_uuid = fake.uuid4()

        organisme = OrganismeRecruteurFactory.create_entity()
        organisme._etapes = (
            EtapeRecrutement.build(
                entity_id=UUID(str(existing_uuid)),
                nom="Réception",
                categorie=CategorieEtapeRecrutement.ENTREE,
            ),
            EtapeRecrutement.build(
                entity_id=UUID(str(new_uuid)),
                nom="Nouvelle étape",
                categorie=CategorieEtapeRecrutement.EN_COURS,
            ),
            EtapeRecrutement.build(
                entity_id=UUID(str(other_uuid)),
                nom="Recrutement",
                categorie=CategorieEtapeRecrutement.ACCEPTE,
            ),
        )

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

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
        assert len(data) == 3  # noqa
        assert data[0]["etape_uuid"] == str(existing_uuid)
        assert data[1]["etape_uuid"] == str(new_uuid)
        assert data[1]["nom"] == "Nouvelle étape"

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_put_returns_400_on_invalid_steps(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = ConfigurationEtapesInvalide(
            "la première étape doit être de catégorie ENTREE"
        )

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

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

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_put_returns_404_when_organisme_not_found(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        payload = [
            {"nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"organisme_uuid": "Not found."}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_put_returns_403_when_not_responsable(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = AccesOrganismeRefuse(UUID(fake.uuid4()))

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        payload = [
            {"nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_put_returns_500_on_unexpected_error(
        self, mock_recruteur_container, authenticated_client
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = Exception("unexpected")

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        payload = [
            {"nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    @patch("presentation.recruteur.views.organismes.recruteur_container")
    def test_forwards_est_staff_to_usecase(
        self, mock_recruteur_container, authenticated_client, test_user
    ):
        test_user.is_staff = True
        test_user.save()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = OrganismeRecruteurFactory.create_entity()

        mock_container = MagicMock()
        mock_container.update_organisme_steps_usecase.return_value = mock_usecase
        mock_recruteur_container.return_value = mock_container

        payload = [
            {"nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Entretien", "categorie": "EN_COURS"},
            {"nom": "Refus", "categorie": "REFUS"},
            {"nom": "Recrutement", "categorie": "ACCEPTE"},
        ]

        authenticated_client.put(ETAPES_URL, payload, format="json")

        command = mock_usecase.execute.call_args.args[0]
        assert command.est_staff is True
