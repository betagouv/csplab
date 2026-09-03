from datetime import datetime
from uuid import uuid4

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory

ORGANISME_UUID = str(uuid4())

AGENTS_URL = reverse(
    "recruteur:organisme-parametres-agents",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)


class TestOrganismeAgentsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert api_client.get(AGENTS_URL).status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_agents_from_real_db(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            username=test_user.username,
            intitule_poste="Chargée de recrutement",
        )
        autre_agent = OrganismeFactory.create_agent_in_organisme(
            organisme.id, role=AgentOrganismeRole.MEMBRE, intitule_poste="Recruteur"
        )
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = {entry["agent_id"]: entry for entry in response.json()}
        assert data.keys() == {
            str(test_user.username),
            str(autre_agent.utilisateur_id),
        }
        assert data[str(test_user.username)] == {
            "agent_id": str(test_user.username),
            "organisme_id": str(organisme.id),
            "nom": test_user.last_name,
            "prenom": test_user.first_name,
            "email": test_user.email,
            "poste": test_user.profil_agent.intitule_poste,
            "role": AgentOrganismeRole.SUPERVISEUR.value,
            "date_derniere_activite": None,
            "date_creation_compte": test_user.date_joined.isoformat().replace(
                "+00:00", "Z"
            ),
            "date_revocation": None,
        }
        assert (
            data[str(autre_agent.utilisateur_id)]["role"]
            == AgentOrganismeRole.MEMBRE.value
        )
        assert data[str(autre_agent.utilisateur_id)]["poste"] == "Recruteur"

    def test_list_agents_excludes_revoked_agent(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            username=test_user.username,
        )
        autre_agent = OrganismeFactory.create_agent_in_organisme(
            organisme.id, role=AgentOrganismeRole.MEMBRE
        )
        OrganismeAgentModel.objects.filter(
            organisme_id=organisme.id, agent_id=autre_agent.utilisateur_id
        ).update(date_revocation=timezone.now())
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        data = {entry["agent_id"]: entry for entry in response.json()}
        assert str(autre_agent.utilisateur_id) not in data

    def test_anonymous_post_is_unauthorized(self, api_client):
        response = api_client.post(AGENTS_URL, data={}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_attach_agent_persists_to_db(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            username=test_user.username,
        )
        bare_agent = AgentFactory.create_model()
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.post(
            url,
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.MEMBRE.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["agent_id"] == str(bare_agent.utilisateur_id)
        assert data["organisme_id"] == str(organisme.id)
        assert data["nom"] == bare_agent.utilisateur.last_name
        assert data["prenom"] == bare_agent.utilisateur.first_name
        assert data["email"] == bare_agent.utilisateur.email
        assert data["poste"] == bare_agent.intitule_poste
        assert data["role"] == AgentOrganismeRole.MEMBRE.value
        assert OrganismeAgentModel.objects.filter(
            organisme_id=organisme.id,
            agent_id=bare_agent.utilisateur_id,
        ).exists()

    def test_attach_agent_forbidden_for_membre(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.MEMBRE,
            username=test_user.username,
        )
        bare_agent = AgentFactory.create_model()
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.post(
            url,
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.MEMBRE.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_attach_agent_already_attached_returns_conflict(
        self, authenticated_client, test_user
    ):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            username=test_user.username,
        )
        autre_agent = OrganismeFactory.create_agent_in_organisme(
            organisme.id, role=AgentOrganismeRole.MEMBRE
        )
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.post(
            url,
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_409_CONFLICT

    def test_attach_agent_unknown_agent_create_agent_too(
        self, authenticated_client, test_user
    ):
        # TODO: to be update when usecase updated too
        pass

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

    def test_update_agent(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            username=test_user.username,
        )
        autre_agent = OrganismeFactory.create_agent_in_organisme(
            organisme.id, role=AgentOrganismeRole.MEMBRE, intitule_poste="Recruteur"
        )
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.put(
            url,
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
                # ignored: role update only, not persisted by this usecase yet
                "poste": "Directeur des recrutements",
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["agent_id"] == str(autre_agent.utilisateur_id)
        assert data["role"] == AgentOrganismeRole.SUPERVISEUR.value
        assert data["poste"] == "Recruteur"
        assert (
            OrganismeAgentModel.objects.get(
                organisme_id=organisme.id, agent_id=autre_agent.utilisateur_id
            ).role
            == AgentOrganismeRole.SUPERVISEUR.value
        )

    def test_update_agent_forbidden_for_membre(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.MEMBRE,
            username=test_user.username,
        )
        autre_agent = OrganismeFactory.create_agent_in_organisme(
            organisme.id, role=AgentOrganismeRole.MEMBRE
        )
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.put(
            url,
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_agent_returns_404_when_not_attached(
        self, authenticated_client, test_user
    ):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            username=test_user.username,
        )
        bare_agent = AgentFactory.create_model()
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.put(
            url,
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

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

    def test_update_agent_requires_role(self, authenticated_client):
        response = authenticated_client.put(
            AGENTS_URL,
            data={"agent_id": str(uuid4())},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_agent_without_revoque_flag_does_not_set_date_revocation(
        self, authenticated_client, test_user
    ):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            username=test_user.username,
        )
        autre_agent = OrganismeFactory.create_agent_in_organisme(
            organisme.id, role=AgentOrganismeRole.MEMBRE
        )
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.put(
            url,
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["date_revocation"] is None
        assert (
            OrganismeAgentModel.objects.get(
                organisme_id=organisme.id, agent_id=autre_agent.utilisateur_id
            ).date_revocation
            is None
        )

    def test_revoke_agent(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            username=test_user.username,
        )
        autre_agent = OrganismeFactory.create_agent_in_organisme(
            organisme.id, role=AgentOrganismeRole.MEMBRE
        )
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.put(
            url,
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.MEMBRE.value,
                "date_revocation": datetime.now(),
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["date_revocation"] is not None
        assert (
            OrganismeAgentModel.objects.get(
                organisme_id=organisme.id, agent_id=autre_agent.utilisateur_id
            ).date_revocation
            is not None
        )

    def test_revoke_agent_forbidden_for_membre(self, authenticated_client, test_user):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.MEMBRE,
            username=test_user.username,
        )
        autre_agent = OrganismeFactory.create_agent_in_organisme(
            organisme.id, role=AgentOrganismeRole.MEMBRE
        )
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.put(
            url,
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.MEMBRE.value,
                "date_revocation": datetime.now(),
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_revoke_agent_returns_404_when_not_attached(
        self, authenticated_client, test_user
    ):
        _, organisme = OrganismeFactory.create_model_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            username=test_user.username,
        )
        bare_agent = AgentFactory.create_model()
        url = reverse(
            "recruteur:organisme-parametres-agents",
            kwargs={"organisme_uuid": str(organisme.id)},
        )

        response = authenticated_client.put(
            url,
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.MEMBRE.value,
                "date_revocation": datetime.now(),
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
