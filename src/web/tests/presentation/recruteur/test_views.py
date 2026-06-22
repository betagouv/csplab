from http import HTTPStatus
from unittest.mock import MagicMock, patch

from django.test import Client
from django.urls import reverse
from faker import Faker
from rest_framework import status

from domain.recruteur.errors.erreur_recrutement import ErreurRecruteur
from tests.factories.recruteur.organisme_factory import (
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

    def test_authenticated_access_is_ok(self, authenticated_client):
        mock_organisme = MagicMock()
        mock_organisme.nom = "COMMUNE DE BRIANCON"
        mock_organisme.siret = "21050023700354"

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = mock_organisme

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase

        with patch(
            "presentation.recruteur.views.recruteur_container",
            return_value=mock_container,
        ):
            response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "nom": "COMMUNE DE BRIANCON",
            "siret": "21050023700354",
        }

    def test_returns_404_when_organisme_not_found(self, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = ErreurRecruteur("not found")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase

        with patch(
            "presentation.recruteur.views.recruteur_container",
            return_value=mock_container,
        ):
            response = authenticated_client.get(ORGANISME_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}


class TestEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_404_when_organisme_not_found(self, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = ErreurRecruteur("not found")

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase

        with patch(
            "presentation.recruteur.views.recruteur_container",
            return_value=mock_container,
        ):
            response = authenticated_client.get(ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"organisme_uuid": "Not found."}

    def test_authenticated_access_is_ok(self, authenticated_client):
        organisme = OrganismeRecruteurFactory.create_entity()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme

        mock_container = MagicMock()
        mock_container.get_organisme_recruteur_usecase.return_value = mock_usecase

        with patch(
            "presentation.recruteur.views.recruteur_container",
            return_value=mock_container,
        ):
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


class TestInitEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(INIT_ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_404_when_organisme_not_found(self, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = ErreurRecruteur("not found")

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase

        with patch(
            "presentation.recruteur.views.recruteur_container",
            return_value=mock_container,
        ):
            response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"organisme_uuid": "Not found."}

    def test_returns_500_on_unexpected_error(self, authenticated_client):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = Exception("unexpected")

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase

        with patch(
            "presentation.recruteur.views.recruteur_container",
            return_value=mock_container,
        ):
            response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    def test_authenticated_post_initialize_steps(self, authenticated_client):
        organisme = OrganismeRecruteurFactory.create_entity()
        organisme.initialiser_etapes()

        mock_usecase = MagicMock()
        mock_usecase.execute.return_value = organisme

        mock_container = MagicMock()
        mock_container.initialize_organisme_steps_usecase.return_value = mock_usecase

        with patch(
            "presentation.recruteur.views.recruteur_container",
            return_value=mock_container,
        ):
            response = authenticated_client.post(INIT_ETAPES_URL)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == [
            {
                "etape_uuid": str(etape.entity_id),
                "nom": etape.nom,
                "categorie": etape.categorie.name,
            }
            for etape in organisme.etapes
        ]


class TestATSBase:
    def test_base_view_returns_200(self, db, client: Client):
        response = client.get("/ats/")
        assert response.status_code == HTTPStatus.OK

    def test_base_view_uses_correct_template(self, db, client: Client):
        response = client.get("/ats/")
        assert "ats/base.html" in [t.name for t in response.templates]

    def test_base_view_catches_subroutes(self, db, client: Client):
        response = client.get("/ats/candidates/123/")
        assert response.status_code == HTTPStatus.OK

    def test_base_view_sets_csrf_cookie(self, db, client: Client):
        response = client.get("/ats/")
        assert "csrftoken" in response.cookies
