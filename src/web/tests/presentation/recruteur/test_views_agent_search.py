from uuid import uuid4

from django.urls import reverse
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory

ORGANISME_UUID = str(uuid4())

AGENT_RECHERCHE_URL = reverse(
    "recruteur:organisme-parametres-agents-recherche",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)


class TestAgentRechercheView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(AGENT_RECHERCHE_URL, {"email": "agent@example.com"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_responsable_finds_agent_by_email(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            username=test_user.username,
        )
        autre_agent = AgentFactory.create_model()
        url = reverse(
            "recruteur:organisme-parametres-agents-recherche",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.get(
            url, {"email": autre_agent.utilisateur.email}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "agent_id": str(autre_agent.utilisateur_id),
            "email": autre_agent.utilisateur.email,
            "prenom": autre_agent.utilisateur.first_name,
            "nom": autre_agent.utilisateur.last_name,
            "intitule_poste": autre_agent.intitule_poste,
        }

    def test_unknown_email_returns_404(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            username=test_user.username,
        )
        url = reverse(
            "recruteur:organisme-parametres-agents-recherche",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.get(url, {"email": "inconnu@example.com"})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "Agent introuvable."}

    def test_unknown_organisme_returns_404(self, authenticated_client):
        organisme_uuid = str(uuid4())
        url = reverse(
            "recruteur:organisme-parametres-agents-recherche",
            kwargs={"organisme_uuid": organisme_uuid},
        )

        response = authenticated_client.get(url, {"email": "agent@example.com"})

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": f"Organisme introuvable : {organisme_uuid}"}

    def test_membre_is_forbidden(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.MEMBRE,
            username=test_user.username,
        )
        url = reverse(
            "recruteur:organisme-parametres-agents-recherche",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.get(url, {"email": "agent@example.com"})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_missing_email_returns_400(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            username=test_user.username,
        )
        url = reverse(
            "recruteur:organisme-parametres-agents-recherche",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_email_returns_400(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            username=test_user.username,
        )
        url = reverse(
            "recruteur:organisme-parametres-agents-recherche",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.get(url, {"email": "not-an-email"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
