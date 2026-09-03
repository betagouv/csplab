from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from django.urls import reverse
from faker import Faker
from rest_framework import status

from application.identite.usecases.create_agent import CreateAgentInput
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.agent_errors import ProfilAgentExisteDeja
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    OperationOrganismeRefusee,
)
from infrastructure.factories.identite.agent_factory import AgentFactory

fake = Faker("fr_FR")

AGENTS_URL = reverse("recruteur:agents")


@pytest.fixture
def container():
    with patch("presentation.recruteur.views.agents.create_identite_container") as mock:
        instance = MagicMock()
        mock.return_value = instance
        yield instance


class TestAgentsView:
    def test_anonymous_access_is_unauthorized(self, api_client):
        response = api_client.post(AGENTS_URL)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_post_create_agent(self, container, authenticated_client):
        mock_usecase = MagicMock()
        agent = AgentFactory.create_entity()
        mock_usecase.execute.return_value = agent
        container.create_agent_usecase.return_value = mock_usecase
        organisme_id = uuid4()
        body = {
            "email": agent.email,
            "prenom": agent.prenom,
            "nom": agent.nom,
            "intitule_poste": agent.intitule_poste,
            "organisme_id": str(organisme_id),
        }

        response = authenticated_client.post(AGENTS_URL, body)

        (called_input,), _ = mock_usecase.execute.call_args
        assert isinstance(called_input, CreateAgentInput)
        assert called_input.email == agent.email
        assert called_input.organisme_id == organisme_id
        assert called_input.utilisateur is not None
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == {
            "agent_id": str(agent.entity_id),
            "email": agent.email,
            "prenom": agent.prenom,
            "nom": agent.nom,
            "intitule_poste": agent.intitule_poste,
        }

    def test_post_missing_field_returns_bad_request(
        self, container, authenticated_client
    ):
        response = authenticated_client.post(AGENTS_URL, {"email": fake.email()})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        container.create_agent_usecase.assert_not_called()

    @pytest.mark.parametrize(
        ("exception", "expected_status", "expected_body"),
        [
            (
                ProfilAgentExisteDeja(fake.email()),
                status.HTTP_400_BAD_REQUEST,
                None,
            ),
            (
                AccesOrganismeRefuse(uuid4()),
                status.HTTP_403_FORBIDDEN,
                None,
            ),
            (
                OperationOrganismeRefusee(),
                status.HTTP_403_FORBIDDEN,
                None,
            ),
            (
                OrganismeNexistePas(str(uuid4())),
                status.HTTP_404_NOT_FOUND,
                {"organisme_id": "Not found."},
            ),
            (
                Exception("unexpected"),
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                {"error": "Unexpected error"},
            ),
        ],
    )
    def test_post_returns_error_from_usecase(
        self,
        container,
        authenticated_client,
        exception,
        expected_status,
        expected_body,
    ):
        mock_usecase = MagicMock()
        mock_usecase.execute.side_effect = exception
        container.create_agent_usecase.return_value = mock_usecase
        body = {
            "email": fake.email(),
            "prenom": fake.first_name(),
            "nom": fake.last_name(),
            "intitule_poste": fake.job(),
            "organisme_id": str(uuid4()),
        }

        response = authenticated_client.post(AGENTS_URL, body)

        assert response.status_code == expected_status
        if expected_body is not None:
            assert response.json() == expected_body
        else:
            assert response.json() == {"error": str(exception)}
