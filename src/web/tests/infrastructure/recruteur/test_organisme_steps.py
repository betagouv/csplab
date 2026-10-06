from unittest.mock import MagicMock

import pytest

from application.recruteur.usecases.update_organisme_steps import (
    UpdateOrganismeStepsCommand,
)
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db):
    container = RecruteurContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(MagicMock(spec=AuditLogWriter))
    return container


@pytest.fixture(name="audited_container")
def audited_container_fixture(db) -> RecruteurContainer:
    container = RecruteurContainer()
    container.app_config.override(AppConfig.from_django_settings())
    container.logger_service.override(LoggerService())
    return container


def _audit_logs(container, organisme_id):
    return container.postgres_audit_log_repository().get_logs_for_ressource(
        "OrganismeRecruteur", organisme_id
    )


def test_update_organisme_steps_logs_action(audited_container):
    etapes = EtapeRecrutementFactory.create_entity_batch()
    agent, organisme_model = create_organisme_with_agent(
        AgentOrganismeRole.SUPERVISEUR, etapes=etapes
    )
    usecase = audited_container.update_organisme_steps_usecase()

    usecase.execute(
        UpdateOrganismeStepsCommand(
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=agent.utilisateur_id
            ),
            organisme_id=organisme_model.id,
            etapes=EtapeRecrutementFactory.to_etape_data_list(etapes),
        )
    )

    logs = _audit_logs(audited_container, organisme_model.id)
    assert len(logs) == 1
    assert logs[0].event_name == "OrganismeEtapesMisesAJour"
    assert logs[0].utilisateur_id == agent.utilisateur_id
    assert logs[0].ressource_id == organisme_model.id


def test_update_organisme_steps(recruteur_integration_container):
    etapes = EtapeRecrutementFactory.create_entity_batch()

    agent, organisme_model = create_organisme_with_agent(
        AgentOrganismeRole.SUPERVISEUR, etapes=etapes
    )

    nouvelles_etapes = EtapeRecrutementFactory.to_etape_data_list(etapes)

    usecase = recruteur_integration_container.update_organisme_steps_usecase()
    organisme = usecase.execute(
        command=UpdateOrganismeStepsCommand(
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=agent.utilisateur_id
            ),
            organisme_id=organisme_model.id,
            etapes=nouvelles_etapes,
        )
    )
    assert organisme.etapes is not None
    assert len(organisme.etapes) == len(nouvelles_etapes)
    usecase.audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=agent.utilisateur_id, aggregate=organisme
    )


class TestUpdateOrganismeStepsRbac:
    def _command(self, organisme, agent, *, etapes, est_staff=False):
        nouvelles_etapes = EtapeRecrutementFactory.to_etape_data_list(etapes)
        return UpdateOrganismeStepsCommand(
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=agent.utilisateur_id, is_staff=est_staff
            ),
            organisme_id=organisme.id,
            etapes=nouvelles_etapes,
        )

    @pytest.mark.parametrize(
        ("role", "est_staff"),
        [(AgentOrganismeRole.SUPERVISEUR, False), (None, True)],
        ids=["responsable", "staff"],
    )
    def test_role_grants_access(self, recruteur_integration_container, role, est_staff):
        etapes = EtapeRecrutementFactory.create_entity_batch()
        agent, organisme = create_organisme_with_agent(role, etapes=etapes)
        usecase = recruteur_integration_container.update_organisme_steps_usecase()

        result = usecase.execute(
            self._command(organisme, agent, etapes=etapes, est_staff=est_staff)
        )

        assert result.etapes is not None

    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.AGENT, None], ids=["membre", "non_membre"]
    )
    def test_role_refuse_access(self, recruteur_integration_container, role):
        etapes = EtapeRecrutementFactory.create_entity_batch()
        agent, organisme = create_organisme_with_agent(role, etapes=etapes)
        usecase = recruteur_integration_container.update_organisme_steps_usecase()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(self._command(organisme, agent, etapes=etapes))
