from unittest.mock import Mock, patch

import pytest

from application.recruteur.usecases.list_organisme_agents import (
    ListOrganismeAgentsQuery,
)
from config.app_config import AppConfig
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.gateways.shared.logger import LoggerService
from infrastructure.mappers.utilisateur_mapper import UtilisateurMapper
from infrastructure.repositories.recruteur.postgres_organisme_agent_query_service import (  # noqa: E501
    PostgresOrganismeAgentQueryService,
)


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


def test_list_organisme_agents_returns_agents_for_responsable(
    db, recruteur_integration_container
):
    agent, organisme_model = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    utilisateur = UtilisateurMapper().to_domain(agent.utilisateur)
    usecase = recruteur_integration_container.list_organisme_agents_usecase()

    result = usecase.execute(
        ListOrganismeAgentsQuery(
            organisme_id=organisme_model.id, utilisateur=utilisateur
        )
    )

    assert len(result) == 1
    agent_organisme = result[0]
    assert agent_organisme.organisme_id == organisme_model.id
    assert agent_organisme.entity_id == agent.utilisateur_id
    assert agent_organisme.nom == agent.utilisateur.last_name
    assert agent_organisme.prenom == agent.utilisateur.first_name
    assert agent_organisme.email == agent.utilisateur.email
    assert agent_organisme.poste == agent.intitule_poste
    assert agent_organisme.role == AgentOrganismeRole.SUPERVISEUR.value

    audit_log_repository = (
        recruteur_integration_container.postgres_audit_log_repository()
    )
    logs = audit_log_repository.get_logs_for_ressource(
        "OrganismeRecruteur", organisme_model.id
    )
    assert len(logs) == 1
    assert logs[0].event_name == "OrganismeAgentsConsultes"
    assert logs[0].utilisateur_id == agent.utilisateur_id
    assert logs[0].ressource_id == organisme_model.id


def test_list_organisme_agents_raises_when_membre(db, recruteur_integration_container):
    agent, organisme_model = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    utilisateur = UtilisateurMapper().to_domain(agent.utilisateur)
    usecase = recruteur_integration_container.list_organisme_agents_usecase()

    with pytest.raises(AccesOrganismeRefuse):
        usecase.execute(
            ListOrganismeAgentsQuery(
                organisme_id=organisme_model.id, utilisateur=utilisateur
            )
        )

    audit_log_repository = (
        recruteur_integration_container.postgres_audit_log_repository()
    )
    assert (
        audit_log_repository.get_logs_for_ressource(
            "OrganismeRecruteur", organisme_model.id
        )
        == []
    )


@patch.object(
    PostgresOrganismeAgentQueryService,
    "list_by_organisme",
    new=Mock(side_effect=RuntimeError("read failed")),
)
def test_list_organisme_agents_does_not_log_when_read_fails(
    db, recruteur_integration_container
):
    agent, organisme_model = create_organisme_with_agent(
        role=AgentOrganismeRole.SUPERVISEUR
    )
    utilisateur = UtilisateurMapper().to_domain(agent.utilisateur)
    usecase = recruteur_integration_container.list_organisme_agents_usecase()

    with pytest.raises(RuntimeError):
        usecase.execute(
            ListOrganismeAgentsQuery(
                organisme_id=organisme_model.id, utilisateur=utilisateur
            )
        )

    audit_log_repository = (
        recruteur_integration_container.postgres_audit_log_repository()
    )
    assert (
        audit_log_repository.get_logs_for_ressource(
            "OrganismeRecruteur", organisme_model.id
        )
        == []
    )
