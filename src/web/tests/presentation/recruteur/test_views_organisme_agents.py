from uuid import uuid4

from django.urls import reverse
from rest_framework import status

ORGANISME_UUID = str(uuid4())

AGENTS_URL = reverse(
    "recruteur:organisme-parametres-agents",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)


class TestOrganismeAgentsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert api_client.get(AGENTS_URL).status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_agents(self, authenticated_client):
        response = authenticated_client.get(AGENTS_URL)

        assert response.status_code == status.HTTP_200_OK
