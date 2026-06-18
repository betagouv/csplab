from http import HTTPStatus

from django.test import Client
from django.urls import reverse
from faker import Faker
from rest_framework import status

fake = Faker()

ORGANISME_UUID = fake.uuid4()
ORGANISME_URL = reverse(
    "recruteur:organisme", kwargs={"organisme_uuid": ORGANISME_UUID}
)
ETAPES_URL = reverse(
    "recruteur:organisme-parametres-etapes",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)


class TestOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ORGANISME_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_access_is_ok(self, authenticated_client):
        response = authenticated_client.get(ORGANISME_URL)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "nom": "COMMUNE DE BRIANCON",
            "siret": "21050023700354",
        }


class TestEtapesRecrutementOrganismeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_authenticated_access_is_ok(self, authenticated_client):
        response = authenticated_client.get(ETAPES_URL)
        assert response.status_code == status.HTTP_200_OK

        results = response.json()
        assert results == [
            {
                "etape_uuid": "11111111-1111-1111-1111-111111111111",
                "nom": "Candidatures ouvertes",
                "categorie": "INITIALE",
            },
            {
                "etape_uuid": "22222222-2222-2222-2222-222222222222",
                "nom": "Entretien",
                "categorie": "EN_COURS",
            },
            {
                "etape_uuid": "33333333-3333-3333-3333-333333333333",
                "nom": "Offre clôturée",
                "categorie": "TERMINALE",
            },
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
