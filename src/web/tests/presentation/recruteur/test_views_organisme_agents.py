from uuid import uuid4

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeAgentModel
from infrastructure.factories.identite.agent_django_factory import (
    AgentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)

ORGANISME_UUID = str(uuid4())

AGENTS_URL = reverse(
    "recruteur:organisme_parametres_agents",
    kwargs={"organisme_uuid": ORGANISME_UUID},
)
SENT_DATE = "2001-01-01T00:00:00Z"
LIST_QUERY_COUNT = 7


def _url(organisme_id):
    return reverse(
        "recruteur:organisme_parametres_agents",
        kwargs={"organisme_uuid": str(organisme_id)},
    )


def _audit_logs():
    return list(
        AuditLogModel.objects.values_list(
            "ressource_kind", "ressource_id", "event_name", "utilisateur_id"
        )
    )


def _liaisons():
    return sorted(
        OrganismeAgentModel.objects.values_list(
            "organisme_id", "agent_id", "role", "date_revocation"
        )
    )


class TestOrganismeAgentsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        assert api_client.get(AGENTS_URL).status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_agents_from_real_db(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
            intitule_poste="Chargée de recrutement",
        )
        autre_agent = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
            agent__intitule_poste="Recruteur",
        ).agent
        OrganismeAgentDjangoFactory(organisme=OrganismeDjangoFactory())

        response = authenticated_client.get(_url(organisme.id))

        assert response.status_code == status.HTTP_200_OK
        data = {entry["uuid"]: entry for entry in response.json()}
        assert data.keys() == {
            str(test_user.username),
            str(autre_agent.utilisateur_id),
        }
        assert data[str(test_user.username)] == {
            "uuid": str(test_user.username),
            "organisme_id": str(organisme.id),
            "nom": test_user.last_name,
            "prenom": test_user.first_name,
            "email": test_user.email,
            "poste": test_user.profil_agent.intitule_poste,
            "role": AgentOrganismeRole.SUPERVISEUR.value,
            "date_derniere_activite": test_user.last_login.isoformat().replace(
                "+00:00", "Z"
            ),
            "date_creation_compte": test_user.date_joined.isoformat().replace(
                "+00:00", "Z"
            ),
            "date_revocation": None,
        }
        assert (
            data[str(autre_agent.utilisateur_id)]["role"]
            == AgentOrganismeRole.AGENT.value
        )
        assert data[str(autre_agent.utilisateur_id)]["poste"] == "Recruteur"
        assert _audit_logs() == [
            (
                "OrganismeRecruteur",
                organisme.id,
                "OrganismeAgentsConsultes",
                test_user.username,
            )
        ]

    def test_list_agents_excludes_revoked_agent(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        autre_agent = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
        ).agent
        OrganismeAgentModel.objects.filter(
            organisme_id=organisme.id, agent_id=autre_agent.utilisateur_id
        ).update(date_revocation=timezone.now())

        response = authenticated_client.get(_url(organisme.id))

        assert response.status_code == status.HTTP_200_OK
        data = {entry["uuid"]: entry for entry in response.json()}
        assert str(autre_agent.utilisateur_id) not in data

    def test_list_agents_query_count_does_not_grow_with_agents(
        self, authenticated_client, test_user, django_assert_num_queries
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        OrganismeAgentDjangoFactory(organisme=organisme)

        with django_assert_num_queries(LIST_QUERY_COUNT):
            assert len(authenticated_client.get(_url(organisme.id)).json()) == 2  # noqa: PLR2004

        OrganismeAgentDjangoFactory(organisme=organisme)

        with django_assert_num_queries(LIST_QUERY_COUNT):
            assert len(authenticated_client.get(_url(organisme.id)).json()) == 3  # noqa: PLR2004

    def test_list_agents_forbidden_for_agent(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT,
            utilisateur=test_user,
        )

        response = authenticated_client.get(_url(organisme.id))

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {"error": "Forbidden."}
        assert _audit_logs() == []

    def test_list_agents_unknown_organisme_returns_404(self, authenticated_client):
        response = authenticated_client.get(AGENTS_URL)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "organisme_uuid: Not found."}
        assert _audit_logs() == []

    def test_anonymous_post_is_unauthorized(self, api_client):
        response = api_client.post(AGENTS_URL, data={}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_attach_agent_persists_to_db(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        bare_agent = AgentDjangoFactory()

        response = authenticated_client.post(
            _url(organisme.id),
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.AGENT.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["uuid"] == str(bare_agent.utilisateur_id)
        assert data["organisme_id"] == str(organisme.id)
        assert data["nom"] == bare_agent.utilisateur.last_name
        assert data["prenom"] == bare_agent.utilisateur.first_name
        assert data["email"] == bare_agent.utilisateur.email
        assert data["poste"] == bare_agent.intitule_poste
        assert data["role"] == AgentOrganismeRole.AGENT.value
        assert OrganismeAgentModel.objects.filter(
            organisme_id=organisme.id,
            agent_id=bare_agent.utilisateur_id,
        ).exists()
        assert _audit_logs() == [
            (
                "AgentOrganisme",
                bare_agent.utilisateur_id,
                "AgentOrganismeRoleAttache",
                test_user.username,
            )
        ]

    def test_attach_agent_reactivates_revoked_agent(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        revoked = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
            date_revocation=timezone.now(),
        )

        response = authenticated_client.post(
            _url(organisme.id),
            data={
                "agent_id": str(revoked.agent_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["role"] == AgentOrganismeRole.SUPERVISEUR.value
        assert response.json()["date_revocation"] is None
        revoked.refresh_from_db()
        assert revoked.role == AgentOrganismeRole.SUPERVISEUR.value
        assert revoked.date_revocation is None
        assert _audit_logs() == [
            (
                "AgentOrganisme",
                revoked.agent_id,
                "AgentOrganismeRoleAttache",
                test_user.username,
            )
        ]

    def test_attach_agent_by_staff(self, api_client):
        staff = UtilisateurDjangoFactory(is_staff=True)
        api_client.force_login(staff)
        organisme = OrganismeDjangoFactory()
        bare_agent = AgentDjangoFactory()

        response = api_client.post(
            _url(organisme.id),
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert OrganismeAgentModel.objects.filter(
            organisme_id=organisme.id,
            agent_id=bare_agent.utilisateur_id,
            role=AgentOrganismeRole.SUPERVISEUR.value,
        ).exists()
        assert _audit_logs() == [
            (
                "AgentOrganisme",
                bare_agent.utilisateur_id,
                "AgentOrganismeRoleAttache",
                staff.username,
            )
        ]

    def test_attach_agent_forbidden_for_membre(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT,
            utilisateur=test_user,
        )
        bare_agent = AgentDjangoFactory()
        liaisons_before = _liaisons()

        response = authenticated_client.post(
            _url(organisme.id),
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.AGENT.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert _liaisons() == liaisons_before
        assert _audit_logs() == []

    def test_attach_agent_already_attached_returns_conflict(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        autre_agent = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
        ).agent
        liaisons_before = _liaisons()

        response = authenticated_client.post(
            _url(organisme.id),
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_409_CONFLICT
        assert response.json() == {
            "error": "agent_id: Agent already attached to this organisme."
        }
        assert _liaisons() == liaisons_before
        assert _audit_logs() == []

    def test_attach_unknown_agent_returns_404(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        liaisons_before = _liaisons()

        response = authenticated_client.post(
            _url(organisme.id),
            data={"agent_id": str(uuid4()), "role": AgentOrganismeRole.AGENT.value},
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "agent_id: Not found."}
        assert _liaisons() == liaisons_before
        assert _audit_logs() == []

    def test_attach_agent_unknown_organisme_returns_404(self, authenticated_client):
        bare_agent = AgentDjangoFactory()

        response = authenticated_client.post(
            AGENTS_URL,
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.AGENT.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "organisme_id: Not found."}
        assert _liaisons() == []
        assert _audit_logs() == []

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
            data={"role": AgentOrganismeRole.AGENT.value},
            format="json",
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_anonymous_put_is_unauthorized(self, api_client):
        response = api_client.put(AGENTS_URL, data={}, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_agent(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        autre_agent = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
            agent__intitule_poste="Recruteur",
        ).agent

        response = authenticated_client.put(
            _url(organisme.id),
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["uuid"] == str(autre_agent.utilisateur_id)
        assert data["role"] == AgentOrganismeRole.SUPERVISEUR.value
        assert data["date_revocation"] is None
        liaison = OrganismeAgentModel.objects.get(
            organisme_id=organisme.id, agent_id=autre_agent.utilisateur_id
        )
        assert liaison.role == AgentOrganismeRole.SUPERVISEUR.value
        assert liaison.date_revocation is None
        assert _audit_logs() == [
            (
                "AgentOrganisme",
                autre_agent.utilisateur_id,
                "AgentOrganismeRoleModifie",
                test_user.username,
            )
        ]

    def test_update_revoked_agent_keeps_revocation(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        revoked_at = timezone.now()
        revoked = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
            date_revocation=revoked_at,
        )

        response = authenticated_client.put(
            _url(organisme.id),
            data={
                "agent_id": str(revoked.agent_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["date_revocation"] is not None
        revoked.refresh_from_db()
        assert revoked.role == AgentOrganismeRole.SUPERVISEUR.value
        assert revoked.date_revocation == revoked_at

    def test_update_agent_forbidden_for_membre(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT,
            utilisateur=test_user,
        )
        autre_agent = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
        ).agent
        liaisons_before = _liaisons()

        response = authenticated_client.put(
            _url(organisme.id),
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert _liaisons() == liaisons_before
        assert _audit_logs() == []

    def test_update_agent_returns_404_when_not_attached(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        bare_agent = AgentDjangoFactory()
        liaisons_before = _liaisons()

        response = authenticated_client.put(
            _url(organisme.id),
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "agent_id: Not found."}
        assert _liaisons() == liaisons_before
        assert _audit_logs() == []

    def test_update_agent_unknown_organisme_returns_404(self, authenticated_client):
        bare_agent = AgentDjangoFactory()

        response = authenticated_client.put(
            AGENTS_URL,
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.SUPERVISEUR.value,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "agent_id: Not found."}
        assert _audit_logs() == []

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
            data={"role": AgentOrganismeRole.AGENT.value},
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

    def test_revoke_agent(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        autre_agent = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
        ).agent
        before = timezone.now()

        response = authenticated_client.put(
            _url(organisme.id),
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.AGENT.value,
                "date_revocation": SENT_DATE,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["date_revocation"] is not None
        liaison = OrganismeAgentModel.objects.get(
            organisme_id=organisme.id, agent_id=autre_agent.utilisateur_id
        )
        assert liaison.date_revocation >= before
        assert _audit_logs() == [
            (
                "AgentOrganisme",
                autre_agent.utilisateur_id,
                "AgentOrganismeRoleRevoque",
                test_user.username,
            )
        ]

    def test_revoke_already_revoked_agent_overwrites_date(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        revoked = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
            date_revocation=timezone.now(),
        )
        before = timezone.now()

        response = authenticated_client.put(
            _url(organisme.id),
            data={
                "agent_id": str(revoked.agent_id),
                "role": AgentOrganismeRole.AGENT.value,
                "date_revocation": SENT_DATE,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        revoked.refresh_from_db()
        assert revoked.date_revocation >= before

    def test_revoke_agent_forbidden_for_membre(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.AGENT,
            utilisateur=test_user,
        )
        autre_agent = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.AGENT.value,
        ).agent
        liaisons_before = _liaisons()

        response = authenticated_client.put(
            _url(organisme.id),
            data={
                "agent_id": str(autre_agent.utilisateur_id),
                "role": AgentOrganismeRole.AGENT.value,
                "date_revocation": SENT_DATE,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert _liaisons() == liaisons_before
        assert _audit_logs() == []

    def test_revoke_agent_returns_404_when_not_attached(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR,
            utilisateur=test_user,
        )
        bare_agent = AgentDjangoFactory()
        liaisons_before = _liaisons()

        response = authenticated_client.put(
            _url(organisme.id),
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.AGENT.value,
                "date_revocation": SENT_DATE,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "agent_id: Not found."}
        assert _liaisons() == liaisons_before
        assert _audit_logs() == []

    def test_revoke_agent_unknown_organisme_returns_404(self, authenticated_client):
        bare_agent = AgentDjangoFactory()

        response = authenticated_client.put(
            AGENTS_URL,
            data={
                "agent_id": str(bare_agent.utilisateur_id),
                "role": AgentOrganismeRole.AGENT.value,
                "date_revocation": SENT_DATE,
            },
            format="json",
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "agent_id: Not found."}
        assert _audit_logs() == []
