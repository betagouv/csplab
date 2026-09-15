from uuid import uuid4

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from domain.recruteur.value_objects.roles import AgentOrganismeRole
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
    RecrutementDjangoFactory,
)


def _url(organisme_uuid):
    return reverse(
        "recruteur:organisme-recrutements-responsable",
        kwargs={"organisme_uuid": organisme_uuid},
    )


class TestRecrutementsResponsableView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        payload = {"recrutement_ids": [], "agent_id": ""}

        response = api_client.put(_url(uuid4()), payload, format="json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_400_for_empty_recrutement_ids(self, authenticated_client):
        payload = {"recrutement_ids": [], "agent_id": str(uuid4())}

        response = authenticated_client.put(_url(uuid4()), payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_for_missing_agent_id(self, authenticated_client):
        payload = {"recrutement_ids": [str(uuid4())]}

        response = authenticated_client.put(_url(uuid4()), payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_for_non_uuid_recrutement_id(self, authenticated_client):
        payload = {"recrutement_ids": ["not-a-uuid"], "agent_id": str(uuid4())}

        response = authenticated_client.put(_url(uuid4()), payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_superviseur_sets_responsable(self, authenticated_client, test_user):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.AGENT.value
        ).agent
        recrutements = [RecrutementDjangoFactory(organisme=organisme) for _ in range(2)]
        payload = {
            "recrutement_ids": [str(r.pk) for r in recrutements],
            "agent_id": str(membre.utilisateur_id),
        }

        response = authenticated_client.put(_url(organisme.id), payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["reussites"] == [str(r.pk) for r in recrutements]
        assert response.data["echecs"] == []

    def test_staff_can_set_responsable_without_organisme_role(self, api_client):
        staff_user = UtilisateurDjangoFactory(is_staff=True)
        refresh = RefreshToken.for_user(staff_user)
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
        organisme = OrganismeDjangoFactory()
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.AGENT.value
        ).agent
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "recrutement_ids": [str(recrutement.pk)],
            "agent_id": str(membre.utilisateur_id),
        }

        response = api_client.put(_url(organisme.id), payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["reussites"] == [str(recrutement.pk)]

    @pytest.mark.parametrize(
        "role",
        [AgentOrganismeRole.AGENT, None],
        ids=["membre_role", "no_organisme_role"],
    )
    def test_is_forbidden_for(self, authenticated_client, test_user, role):
        if role is None:
            organisme = OrganismeDjangoFactory()
        else:
            _, organisme = create_organisme_with_agent(role=role, utilisateur=test_user)
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.AGENT.value
        ).agent
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "recrutement_ids": [str(recrutement.pk)],
            "agent_id": str(membre.utilisateur_id),
        }

        response = authenticated_client.put(_url(organisme.id), payload, format="json")

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_returns_404_for_unknown_organisme(self, authenticated_client):
        payload = {"recrutement_ids": [str(uuid4())], "agent_id": str(uuid4())}

        response = authenticated_client.put(_url(uuid4()), payload, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_echec_for_recrutement_belonging_to_another_organisme(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        membre = OrganismeAgentDjangoFactory(
            organisme=organisme, role=AgentOrganismeRole.AGENT.value
        ).agent
        valide = RecrutementDjangoFactory(organisme=organisme)
        autre_organisme = OrganismeDjangoFactory()
        invalide = RecrutementDjangoFactory(organisme=autre_organisme)
        payload = {
            "recrutement_ids": [str(valide.pk), str(invalide.pk)],
            "agent_id": str(membre.utilisateur_id),
        }

        response = authenticated_client.put(_url(organisme.id), payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        echec_ids = [echec["recrutement_uuid"] for echec in response.data["echecs"]]
        assert response.data["reussites"] == [str(valide.pk)]
        assert echec_ids == [str(invalide.pk)]
        assert response.data["echecs"][0]["raison"]

    def test_processes_recrutement_when_agent_not_yet_attached_to_organisme(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        bare_agent = AgentDjangoFactory()
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "recrutement_ids": [str(recrutement.pk)],
            "agent_id": str(bare_agent.utilisateur_id),
        }

        response = authenticated_client.put(_url(organisme.id), payload, format="json")

        assert response.status_code == status.HTTP_200_OK
        assert response.data["reussites"] == [str(recrutement.pk)]

    def test_returns_404_when_agent_does_not_exist(
        self, authenticated_client, test_user
    ):
        _, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, utilisateur=test_user
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        payload = {
            "recrutement_ids": [str(recrutement.pk)],
            "agent_id": str(uuid4()),
        }

        response = authenticated_client.put(_url(organisme.id), payload, format="json")

        assert response.status_code == status.HTTP_404_NOT_FOUND
