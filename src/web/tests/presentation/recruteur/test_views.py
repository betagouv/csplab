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
RECRUTEMENTS_URL = reverse(
    "recruteur:organisme-recrutements",
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

    def test_put_mixed_existing_and_new_etapes(self, authenticated_client):
        existing_uuid = str(fake.uuid4())
        payload = [
            {"etape_uuid": existing_uuid, "nom": "Réception", "categorie": "ENTREE"},
            {"nom": "Nouvelle étape", "categorie": "EN_COURS"},
            {
                "etape_uuid": str(fake.uuid4()),
                "nom": "Recrutement",
                "categorie": "TERMINALE",
            },
        ]

        response = authenticated_client.put(ETAPES_URL, payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3  # noqa
        assert data[0]["etape_uuid"] == existing_uuid
        assert data[1]["etape_uuid"] is not None
        assert data[1]["nom"] == "Nouvelle étape"


class TestRecrutementsOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(RECRUTEMENTS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_actifs_by_default(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENTS_URL)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "count" in data
        assert "next" in data
        assert "previous" in data
        assert "results" in data
        assert data["count"] == 6  # noqa
        assert len(data["results"]) == 6  # noqa

    def test_returns_actifs_with_explicit_filtre(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENTS_URL + "?filtre=actifs")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 6  # noqa
        first = data["results"][0]
        assert "offer_id" in first
        assert "intitule" in first
        assert "reference_csp" in first
        assert "type_contrat" in first
        assert "kind_contrat" in first
        assert "date_publication" in first
        assert "responsables" in first
        assert "derniere_activite" in first
        assert "candidatures" in first

    def test_returns_archives_with_filtre_archives(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENTS_URL + "?filtre=archives")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["count"] == 3  # noqa
        first = data["results"][0]
        assert "finalise" in first
        assert "recrute" in first

    def test_candidatures_structure(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENTS_URL)
        data = response.json()
        candidatures = data["results"][0]["candidatures"]
        assert "total" in candidatures
        assert "a_traiter" in candidatures
        assert "en_cours" in candidatures

    def test_pagination_second_page(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENTS_URL + "?size=2&page=2")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["results"]) == 2  # noqa
        assert data["next"] is not None
        assert data["previous"] is not None

    def test_invalid_filtre_returns_400(self, authenticated_client):
        response = authenticated_client.get(RECRUTEMENTS_URL + "?filtre=inconnu")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


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
