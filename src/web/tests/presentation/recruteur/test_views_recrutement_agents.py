from datetime import datetime
from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.recruteur.models.recrutement import (
    RecrutementAgentModel,
)
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)

UNSET = object()

NOMBRE_AGENTS_ATTENDU = 2
NOMBRE_REQUETES_ATTENDU = (
    2  # authentification
    + 1  # organisme
    + 1  # agent's role
    + 1  # matching recrutement with organisme
    + 2  # pagination : count + page
)


def _url(organisme_uuid, recrutement_uuid):
    return reverse(
        "recruteur:organisme-recrutement-parametres-agents",
        kwargs={"organisme_uuid": organisme_uuid, "recrutement_uuid": recrutement_uuid},
    )


def _unknown_organisme_ids(organisme):
    return uuid4(), uuid4()


def _unknown_recrutement_ids(organisme):
    return organisme.id, uuid4()


def _recrutement_from_another_organisme_ids(organisme):
    autre_organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=autre_organisme)
    return organisme.id, recrutement.pk


class TestRecrutementAgentsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.get(_url(uuid4(), uuid4()))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_responsable_lists_recrutement_agents(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            utilisateur=test_user,
        )
        membre = AgentDjangoFactory()
        recrutement = RecrutementDjangoFactory(
            organisme=organisme,
            agent_link__agent=membre,
            agent_link__role=AgentRecrutementRole.RESPONSABLE.value,
        )

        response = authenticated_client.get(_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["count"] == 1
        assert body["results"] == [
            {
                "agent_id": str(membre.utilisateur_id),
                "nom": membre.utilisateur.last_name,
                "prenom": membre.utilisateur.first_name,
                "poste": membre.intitule_poste,
                "email": membre.utilisateur.email,
                "recrutement_role": AgentRecrutementRole.RESPONSABLE.value,
            }
        ]

    def test_lists_every_agent_of_the_recrutement(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            utilisateur=test_user,
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        RecrutementAgentDjangoFactory(
            recrutement=recrutement, role=AgentRecrutementRole.CONTRIBUTEUR.value
        )

        response = authenticated_client.get(_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK
        results = response.json()["results"]
        assert len(results) == NOMBRE_AGENTS_ATTENDU
        assert {r["recrutement_role"] for r in results} == {
            AgentRecrutementRole.CONTRIBUTEUR.value
        }

    def test_staff_can_list_without_organisme_role(self, api_client):
        staff_user = UtilisateurDjangoFactory(is_staff=True)
        refresh = RefreshToken.for_user(staff_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        organisme = OrganismeDjangoFactory()
        recrutement = RecrutementDjangoFactory(organisme=organisme)

        response = api_client.get(_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "role",
        [AgentOrganismeRole.MEMBRE, None],
        ids=["membre_role", "no_organisme_role"],
    )
    def test_is_forbidden_for(self, authenticated_client, test_user, role):
        if role is None:
            organisme = OrganismeDjangoFactory()
        else:
            _, organisme = create_organisme_with_agent(role=role, utilisateur=test_user)
        recrutement = RecrutementDjangoFactory(organisme=organisme)

        response = authenticated_client.get(_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        "build_ids",
        [
            _unknown_organisme_ids,
            _unknown_recrutement_ids,
            _recrutement_from_another_organisme_ids,
        ],
        ids=[
            "unknown_organisme",
            "unknown_recrutement",
            "recrutement_from_another_organisme",
        ],
    )
    def test_returns_404_for(self, authenticated_client, test_user, build_ids):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            utilisateur=test_user,
        )
        organisme_uuid, recrutement_uuid = build_ids(organisme)

        response = authenticated_client.get(_url(organisme_uuid, recrutement_uuid))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_does_not_trigger_n_plus_one_queries(
        self, authenticated_client, test_user, django_assert_num_queries
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE,
            utilisateur=test_user,
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        RecrutementAgentDjangoFactory.create_batch(5, recrutement=recrutement)

        with django_assert_num_queries(NOMBRE_REQUETES_ATTENDU):
            response = authenticated_client.get(_url(organisme.id, recrutement.pk))

        assert response.status_code == status.HTTP_200_OK


class TestRecrutementAgentsViewPost:
    def test_anonymous_access_is_unauthorized(self, api_client):
        payload = {
            "agent_id": str(uuid4()),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }

        response = api_client.post(_url(uuid4(), uuid4()), payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_400_for_invalid_role(self, authenticated_client):
        payload = {"agent_id": str(uuid4()), "recrutement_role": "inconnu"}

        response = authenticated_client.post(_url(uuid4(), uuid4()), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_for_missing_agent_id(self, authenticated_client):
        payload = {"recrutement_role": AgentRecrutementRole.RECRUTEUR.value}

        response = authenticated_client.post(_url(uuid4(), uuid4()), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_201_with_recrutement_agent_shape_for_valid_payload(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE, utilisateur=test_user
        )
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
        ).agent
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "agent_id": str(membre.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }

        response = authenticated_client.post(
            _url(organisme.id, recrutement.pk), payload
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "agent_id": str(membre.utilisateur_id),
            "nom": membre.utilisateur.last_name,
            "prenom": membre.utilisateur.first_name,
            "poste": membre.intitule_poste,
            "email": membre.utilisateur.email,
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }
        assert RecrutementAgentModel.objects.filter(
            recrutement=recrutement, agent=membre
        ).exists()

    def test_staff_can_add_agent_without_organisme_role(self, api_client):
        staff_user = UtilisateurDjangoFactory(is_staff=True)
        refresh = RefreshToken.for_user(staff_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        organisme = OrganismeDjangoFactory()
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
        ).agent
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "agent_id": str(membre.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.CONTRIBUTEUR.value,
        }

        response = api_client.post(_url(organisme.id, recrutement.pk), payload)

        assert response.status_code == status.HTTP_201_CREATED

    @pytest.mark.parametrize(
        "role",
        [AgentOrganismeRole.MEMBRE, None],
        ids=["membre_role", "no_organisme_role"],
    )
    def test_is_forbidden_for(self, authenticated_client, test_user, role):
        if role is None:
            organisme = OrganismeDjangoFactory()
        else:
            _, organisme = create_organisme_with_agent(role=role, utilisateur=test_user)
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
        ).agent
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "agent_id": str(membre.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.CONTRIBUTEUR.value,
        }

        response = authenticated_client.post(
            _url(organisme.id, recrutement.pk), payload
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        "build_ids",
        [
            _unknown_organisme_ids,
            _unknown_recrutement_ids,
            _recrutement_from_another_organisme_ids,
        ],
        ids=[
            "unknown_organisme",
            "unknown_recrutement",
            "recrutement_from_another_organisme",
        ],
    )
    def test_returns_404_for_organisme_or_recrutement(
        self, authenticated_client, test_user, build_ids
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE, utilisateur=test_user
        )
        organisme_uuid, recrutement_uuid = build_ids(organisme)
        payload = {
            "agent_id": str(uuid4()),
            "recrutement_role": AgentRecrutementRole.CONTRIBUTEUR.value,
        }

        response = authenticated_client.post(
            _url(organisme_uuid, recrutement_uuid), payload
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_404_when_agent_to_add_does_not_exist(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "agent_id": str(uuid4()),
            "recrutement_role": AgentRecrutementRole.CONTRIBUTEUR.value,
        }

        response = authenticated_client.post(
            _url(organisme.id, recrutement.pk), payload
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_404_when_agent_to_add_is_not_attached_to_organisme(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE, utilisateur=test_user
        )
        bare_agent = AgentDjangoFactory()
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "agent_id": str(bare_agent.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.CONTRIBUTEUR.value,
        }

        response = authenticated_client.post(
            _url(organisme.id, recrutement.pk), payload
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_409_when_agent_already_member_of_recrutement(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        deja_membre = RecrutementAgentModel.objects.get(recrutement=recrutement).agent
        OrganismeAgentDjangoFactory(
            organisme=organisme, agent=deja_membre, role=AgentOrganismeRole.MEMBRE.value
        )
        payload = {
            "agent_id": str(deja_membre.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.CONTRIBUTEUR.value,
        }

        response = authenticated_client.post(
            _url(organisme.id, recrutement.pk), payload
        )

        assert response.status_code == status.HTTP_409_CONFLICT


class TestRecrutementAgentsViewPut:
    def test_anonymous_access_is_unauthorized(self, api_client):
        payload = {
            "agent_id": str(uuid4()),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }

        response = api_client.put(_url(uuid4(), uuid4()), payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_400_for_invalid_role(self, authenticated_client):
        payload = {"agent_id": str(uuid4()), "recrutement_role": "inconnu"}

        response = authenticated_client.put(_url(uuid4(), uuid4()), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_for_missing_agent_id(self, authenticated_client):
        payload = {"recrutement_role": AgentRecrutementRole.RECRUTEUR.value}

        response = authenticated_client.put(_url(uuid4(), uuid4()), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_for_invalid_date_revocation_recrutement(
        self, authenticated_client
    ):
        payload = {
            "agent_id": str(uuid4()),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
            "date_revocation_recrutement": "invalide",
        }

        response = authenticated_client.put(_url(uuid4(), uuid4()), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_200_with_revocation_date(self, authenticated_client):
        agent_id = uuid4()
        payload = {
            "agent_id": str(agent_id),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
            "date_revocation_recrutement": datetime.now(),
        }

        response = authenticated_client.put(
            _url(uuid4(), uuid4()), payload, format="json"
        )

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["agent_id"] == str(agent_id)
        assert body["recrutement_role"] == AgentRecrutementRole.RECRUTEUR.value
        assert body["date_revocation_recrutement"] is not None

    def test_responsable_updates_agent_role(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE, utilisateur=test_user
        )
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
        ).agent
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        RecrutementAgentDjangoFactory(
            recrutement=recrutement,
            agent=membre,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )
        payload = {
            "agent_id": str(membre.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }

        response = authenticated_client.put(_url(organisme.id, recrutement.pk), payload)

        assert response.status_code == status.HTTP_200_OK
        body = response.json()
        assert body["agent_id"] == str(membre.utilisateur_id)
        assert body["recrutement_role"] == AgentRecrutementRole.RECRUTEUR.value
        assert (
            RecrutementAgentModel.objects.get(
                recrutement=recrutement, agent=membre
            ).role
            == AgentRecrutementRole.RECRUTEUR.value
        )

    def test_staff_can_update_agent_without_organisme_role(self, api_client):
        staff_user = UtilisateurDjangoFactory(is_staff=True)
        refresh = RefreshToken.for_user(staff_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        organisme = OrganismeDjangoFactory()
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
        ).agent
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        RecrutementAgentDjangoFactory(
            recrutement=recrutement,
            agent=membre,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )
        payload = {
            "agent_id": str(membre.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }

        response = api_client.put(_url(organisme.id, recrutement.pk), payload)

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize(
        "role",
        [AgentOrganismeRole.MEMBRE, None],
        ids=["membre_role", "no_organisme_role"],
    )
    def test_is_forbidden_for(self, authenticated_client, test_user, role):
        if role is None:
            organisme = OrganismeDjangoFactory()
        else:
            _, organisme = create_organisme_with_agent(role=role, utilisateur=test_user)
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
        ).agent
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        RecrutementAgentDjangoFactory(
            recrutement=recrutement,
            agent=membre,
            role=AgentRecrutementRole.CONTRIBUTEUR.value,
        )
        payload = {
            "agent_id": str(membre.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }

        response = authenticated_client.put(_url(organisme.id, recrutement.pk), payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        "build_ids",
        [
            _unknown_organisme_ids,
            _unknown_recrutement_ids,
            _recrutement_from_another_organisme_ids,
        ],
        ids=[
            "unknown_organisme",
            "unknown_recrutement",
            "recrutement_from_another_organisme",
        ],
    )
    def test_returns_404_for_organisme_or_recrutement(
        self, authenticated_client, test_user, build_ids
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE, utilisateur=test_user
        )
        organisme_uuid, recrutement_uuid = build_ids(organisme)
        payload = {
            "agent_id": str(uuid4()),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }

        response = authenticated_client.put(
            _url(organisme_uuid, recrutement_uuid), payload
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_404_when_agent_to_update_is_not_attached_to_organisme(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE, utilisateur=test_user
        )
        bare_agent = AgentDjangoFactory()
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "agent_id": str(bare_agent.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }

        response = authenticated_client.put(_url(organisme.id, recrutement.pk), payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_404_when_agent_is_not_member_of_recrutement(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE, utilisateur=test_user
        )
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.MEMBRE.value
        ).agent
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "agent_id": str(membre.utilisateur_id),
            "recrutement_role": AgentRecrutementRole.RECRUTEUR.value,
        }

        response = authenticated_client.put(_url(organisme.id, recrutement.pk), payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND
