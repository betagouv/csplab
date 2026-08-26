import pytest

from config.app_config import AppConfig
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.repositories.recruteur.postgres_organisme_agent_query_service import (  # noqa: E501
    PostgresOrganismeAgentQueryService,
)


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


@pytest.fixture(name="service")
def service_fixture(
    recruteur_integration_container,
) -> PostgresOrganismeAgentQueryService:
    return recruteur_integration_container.postgres_organisme_agent_query_service()


def test_list_by_organisme_returns_agents(db, service):
    agent, organisme_model = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.RESPONSABLE
    )

    agents = service.list_by_organisme(organisme_id=organisme_model.id)

    assert len(agents) == 1
    agent_organisme = agents[0]
    assert agent_organisme.organisme_id == organisme_model.id
    assert agent_organisme.entity_id == agent.utilisateur_id
    assert agent_organisme.nom == agent.utilisateur.last_name
    assert agent_organisme.prenom == agent.utilisateur.first_name
    assert agent_organisme.email == agent.utilisateur.email
    assert agent_organisme.poste == agent.intitule_poste
    assert agent_organisme.role == AgentOrganismeRole.RESPONSABLE.value


def test_list_by_organisme_returns_empty_when_no_agent(db, service):
    organisme_model = OrganismeFactory.create_model()

    agents = service.list_by_organisme(organisme_id=organisme_model.id)

    assert agents == []
