from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.recruteur.dtos.etape_data import EtapeData
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)

fake = Faker()

ORGANISME_UUID = fake.uuid4()

# UUID du recrutement statique défini dans views.py
RECRUTEMENT_UUID = "aaaaaaaa-0001-0001-0001-000000000001"

RECRUTEMENT_ETAPES_URL = reverse(
    "recruteur:organisme-recrutement-etapes",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)
RECRUTEMENT_ETAPES_INIT_URL = reverse(
    "recruteur:organisme-recrutement-etapes-init",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)


@pytest.fixture
def container():
    with patch(
        "presentation.recruteur.views.recrutement_params.recruteur_container"
    ) as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


NB_ETAPES_STUB = 2


def _etapes_stub() -> list[EtapeData]:
    return [
        EtapeData(
            etape_uuid=uuid4(),
            nom="Réception des candidatures",
            categorie=CategorieEtapeRecrutement.ENTREE,
        ),
        EtapeData(
            etape_uuid=uuid4(),
            nom="Recrutement",
            categorie=CategorieEtapeRecrutement.ACCEPTE,
        ),
    ]


class TestRecrutementEtapeView:
    def test_anonymous_access_is_unauthorized_on_get(self, api_client):
        response = api_client.get(RECRUTEMENT_ETAPES_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_access_is_unauthorized_on_patch(self, api_client):
        response = api_client.patch(RECRUTEMENT_ETAPES_URL, data=[], format="json")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_returns_default_pipeline(self, container, authenticated_client):
        etapes = _etapes_stub()
        container.get_recrutement_etapes_usecase.return_value.execute.return_value = (
            etapes
        )

        response = authenticated_client.get(RECRUTEMENT_ETAPES_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == NB_ETAPES_STUB
        assert data[0]["nom"] == "Réception des candidatures"
        assert data[0]["categorie"] == "ENTREE"

    def test_get_returns_404_for_unknown_organisme(
        self, container, authenticated_client
    ):
        container.get_recrutement_etapes_usecase.return_value.execute.side_effect = (
            OrganismeNexistePas("not found")
        )

        response = authenticated_client.get(RECRUTEMENT_ETAPES_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_get_returns_403_when_forbidden(self, container, authenticated_client):
        container.get_recrutement_etapes_usecase.return_value.execute.side_effect = (
            AccesOrganismeRefuse(uuid4())
        )

        response = authenticated_client.get(RECRUTEMENT_ETAPES_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    def test_get_returns_500_on_unexpected_error(self, container, authenticated_client):
        container.get_recrutement_etapes_usecase.return_value.execute.side_effect = (
            Exception("unexpected")
        )

        response = authenticated_client.get(RECRUTEMENT_ETAPES_URL)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}

    def test_patch_requires_valid_body(self, authenticated_client):
        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=[{"nom": "Réception"}],
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_patch_returns_404_for_unknown_organisme(
        self, container, authenticated_client
    ):
        container.update_recrutement_etapes_usecase.return_value.execute.side_effect = (
            OrganismeNexistePas("not found")
        )

        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=[{"nom": "Réception", "categorie": "ENTREE"}],
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_patch_returns_403_when_forbidden(self, container, authenticated_client):
        container.update_recrutement_etapes_usecase.return_value.execute.side_effect = (
            AccesOrganismeRefuse(uuid4())
        )

        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=[{"nom": "Réception", "categorie": "ENTREE"}],
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    def test_patch_returns_500_on_unexpected_error(
        self, container, authenticated_client
    ):
        container.update_recrutement_etapes_usecase.return_value.execute.side_effect = (
            Exception("unexpected")
        )

        response = authenticated_client.patch(
            RECRUTEMENT_ETAPES_URL,
            data=[{"nom": "Réception", "categorie": "ENTREE"}],
            format="json",
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}


class TestInitRecrutementEtapeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(RECRUTEMENT_ETAPES_INIT_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_201_with_default_pipeline(self, container, authenticated_client):
        etapes = _etapes_stub()
        container.init_recrutement_etapes_usecase.return_value.execute.return_value = (
            etapes
        )

        response = authenticated_client.post(RECRUTEMENT_ETAPES_INIT_URL)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert len(data) == NB_ETAPES_STUB
        assert data[1]["nom"] == "Recrutement"
        assert data[1]["categorie"] == "ACCEPTE"

    def test_returns_404_for_unknown_organisme(self, container, authenticated_client):
        container.init_recrutement_etapes_usecase.return_value.execute.side_effect = (
            OrganismeNexistePas("not found")
        )

        response = authenticated_client.post(RECRUTEMENT_ETAPES_INIT_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_returns_403_when_forbidden(self, container, authenticated_client):
        container.init_recrutement_etapes_usecase.return_value.execute.side_effect = (
            AccesOrganismeRefuse(uuid4())
        )

        response = authenticated_client.post(RECRUTEMENT_ETAPES_INIT_URL)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"detail": "Forbidden."}

    def test_returns_500_on_unexpected_error(self, container, authenticated_client):
        container.init_recrutement_etapes_usecase.return_value.execute.side_effect = (
            Exception("unexpected")
        )

        response = authenticated_client.post(RECRUTEMENT_ETAPES_INIT_URL)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}
