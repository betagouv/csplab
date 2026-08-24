from uuid import uuid4

from django.urls import reverse
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole

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

    def test_anonymous_post_is_unauthorized(self, api_client):
        response = api_client.post(AGENTS_URL, data={}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_set_agent_role(self, authenticated_client):
        agent_id = str(uuid4())

        response = authenticated_client.post(
            AGENTS_URL,
            data={"agent_id": agent_id, "role": AgentOrganismeRole.MEMBRE.value},
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["agent_id"] == agent_id
        assert data["role"] == AgentOrganismeRole.MEMBRE.value

    def test_set_agent_role_invalid_role(self, authenticated_client):
        response = authenticated_client.post(
            AGENTS_URL,
            data={"agent_id": str(uuid4()), "role": "not-a-role"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_set_agent_role_requires_agent_id(self, authenticated_client):
        response = authenticated_client.post(
            AGENTS_URL,
            data={"role": AgentOrganismeRole.MEMBRE.value},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anonymous_put_is_unauthorized(self, api_client):
        response = api_client.put(AGENTS_URL, data={}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_agent(self, authenticated_client):
        agent_id = str(uuid4())

        response = authenticated_client.put(
            AGENTS_URL,
            data={
                "agent_id": agent_id,
                "role": AgentOrganismeRole.RESPONSABLE.value,
                "poste": "Directeur des recrutements",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["agent_id"] == agent_id
        assert data["role"] == AgentOrganismeRole.RESPONSABLE.value
        assert data["poste"] == "Directeur des recrutements"

    def test_update_agent_invalid_role(self, authenticated_client):
        response = authenticated_client.put(
            AGENTS_URL,
            data={"agent_id": str(uuid4()), "role": "not-a-role"},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_agent_requires_agent_id(self, authenticated_client):
        response = authenticated_client.put(
            AGENTS_URL,
            data={"role": AgentOrganismeRole.MEMBRE.value},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_revoke_agent_role_on_organisme(self, authenticated_client):
        agent_id = str(uuid4())

        response = authenticated_client.put(
            AGENTS_URL,
            data={
                "agent_id": agent_id,
                "date_revocation": "2026-08-20T10:00:00Z",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["agent_id"] == agent_id
        assert data["date_revocation"] == "2026-08-20T10:00:00Z"
