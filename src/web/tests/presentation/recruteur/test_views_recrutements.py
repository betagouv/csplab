from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from domain.identite.errors.organisme_errors import OrganismeNexistePas

fake = Faker()

ORGANISME_UUID = fake.uuid4()
UNKNOWN_ORGANISME_UUID = fake.uuid4()

# UUID du recrutement statique défini dans views.py
RECRUTEMENT_UUID = "aaaaaaaa-0001-0001-0001-000000000001"

RECRUTEMENT_CANDIDATURES_ETAPE_URL = reverse(
    "recruteur:organisme-recrutement-candidatures-etape",
    kwargs={"organisme_uuid": ORGANISME_UUID, "recrutement_uuid": RECRUTEMENT_UUID},
)


@pytest.fixture
def container():
    with patch("presentation.recruteur.views.recrutements.recruteur_container") as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


class TestRecrutementCandidaturesEtapeView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_echoes_candidatures_as_reussites(self, container, authenticated_client):
        candidature_uuid = str(uuid4())
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
        mock_usecase.execute.return_value = MagicMock(
            reussites=[UUID(candidature_uuid)], echecs=[]
        )

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={
                "etape_cible_uuid": fake.uuid4(),
                "candidatures": [
                    {
                        "candidature_uuid": candidature_uuid,
                        "etape_actuelle_uuid": fake.uuid4(),
                    }
                ],
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["reussites"] == [candidature_uuid]
        assert data["echecs"] == []

    def test_requires_etape_cible_uuid(self, authenticated_client):
        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"candidatures": []},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_404_for_unknown_organisme(self, container, authenticated_client):
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
        mock_usecase.execute.side_effect = OrganismeNexistePas("not found")

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Not found."}

    def test_returns_500_on_unexpected_error(self, container, authenticated_client):
        mock_usecase = container.changer_etape_candidatures_usecase.return_value
        mock_usecase.execute.side_effect = Exception("unexpected")

        response = authenticated_client.patch(
            RECRUTEMENT_CANDIDATURES_ETAPE_URL,
            data={"etape_cible_uuid": fake.uuid4(), "candidatures": []},
            format="json",
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.json() == {"error": "Unexpected error"}
