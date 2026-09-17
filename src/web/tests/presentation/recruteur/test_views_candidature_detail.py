from uuid import uuid4

from django.urls import reverse
from rest_framework import status

ORGANISME_UUID = str(uuid4())
RECRUTEMENT_UUID = str(uuid4())
CANDIDATURE_UUID = str(uuid4())

CANDIDATURE_DETAIL_URL = reverse(
    "recruteur:organisme-recrutement-candidature-detail",
    kwargs={
        "organisme_uuid": ORGANISME_UUID,
        "recrutement_uuid": RECRUTEMENT_UUID,
        "candidature_uuid": CANDIDATURE_UUID,
    },
)


class TestCandidatureDetailView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(CANDIDATURE_DETAIL_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_200_with_stub_payload(self, authenticated_client):
        response = authenticated_client.get(CANDIDATURE_DETAIL_URL)

        assert response.status_code == status.HTTP_200_OK
        data = response.data
        assert data["candidature_id"] == CANDIDATURE_UUID
        assert set(data["candidat"].keys()) == {"id", "prenom", "nom", "email"}
        assert data["recrutement_intitule"]
        assert len(data["etapes"]) >= 1
        assert set(data["etape_actuelle"].keys()) == {"etape_id", "nom"}
        assert data["etape_actuelle"] in data["etapes"]
        assert data["date_candidature"] is not None
        assert data["document_id"]

    def test_navigation_includes_current_candidature(self, authenticated_client):
        response = authenticated_client.get(CANDIDATURE_DETAIL_URL)

        assert CANDIDATURE_UUID in response.data["navigation_candidature_ids"]
