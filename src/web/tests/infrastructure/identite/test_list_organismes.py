from unittest.mock import Mock

import pytest

from application.identite.usecases.list_organismes import (
    ListOrganismesCommand,
)
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="organismes")
def organismes_list_fixture():
    return OrganismeFactory.create_model_batch()


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(Mock(spec=AuditLogWriter))
    return container


def test_list_organismes(db, organismes, identite_integration_container):
    command = ListOrganismesCommand(
        utilisateur=UtilisateurFactory.create_entity(is_staff=True),
    )

    result = identite_integration_container.list_organismes_usecase().execute(command)

    assert len(result) == len(organismes)
    result_ids = {r.entity_id for r in result}
    organism_ids = {o.id for o in organismes}
    assert result_ids == organism_ids

    for organisme in result:
        assert organisme.number_agents == 0
        assert organisme.number_published_offers == 0


def test_list_organismes_with_counts(db, identite_integration_container):
    _, organisme_with_agents = OrganismeFactory.create_model_with_agent(
        role=AgentOrganismeRole.MEMBRE,
    )
    OrganismeFactory.create_model_with_agent(role=AgentOrganismeRole.MEMBRE)

    organisme_with_recruitments = OrganismeFactory.create_model()
    RecrutementFactory.create_model(organisme_id=organisme_with_recruitments.id)
    RecrutementFactory.create_model(organisme_id=organisme_with_recruitments.id)

    command = ListOrganismesCommand(
        utilisateur=UtilisateurFactory.create_entity(is_staff=True),
    )

    result = identite_integration_container.list_organismes_usecase().execute(command)

    organisme_with_agents_result = next(
        r for r in result if r.entity_id == organisme_with_agents.id
    )
    assert organisme_with_agents_result.number_agents == 1
    assert organisme_with_agents_result.number_published_offers == 0

    organisme_with_offers_result = next(
        r for r in result if r.entity_id == organisme_with_recruitments.id
    )
    assert organisme_with_offers_result.number_agents == 0
    assert organisme_with_offers_result.number_published_offers == 2  # noqa


def test_list_organismes_refuse_non_staff(db, identite_integration_container):
    command = ListOrganismesCommand(
        utilisateur=UtilisateurFactory.create_entity(is_staff=False),
    )

    with pytest.raises(OperationOrganismeRefusee):
        identite_integration_container.list_organismes_usecase().execute(command)
