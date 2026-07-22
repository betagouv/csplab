from unittest.mock import MagicMock
from uuid import UUID

import pytest

from application.recruteur.usecases.get_organisme_recruteur import (
    GetOrganismeRecruteurQuery,
)
from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from application.recruteur.usecases.update_organisme_steps import (
    UpdateOrganismeStepsCommand,
)
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.identite.agent_factory import AgentFactory
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.gateways.shared.logger import LoggerService

NB_ETAPES_PAR_DEFAUT = 6


def _create_agent(role: AgentOrganismeRole | None = None, **organisme_kwargs):
    agent = AgentFactory.create_model()
    if role is not None:
        organisme = OrganismeFactory.create_model(
            agent_id=UUID(agent.utilisateur_id), role=role, **organisme_kwargs
        )
    else:
        organisme = OrganismeFactory.create_model(**organisme_kwargs)
    return agent, organisme


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db):
    container = RecruteurContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(MagicMock(spec=AuditLogWriter))
    return container


def test_get_organisme_steps(recruteur_integration_container):
    agent, organisme_model = _create_agent(AgentOrganismeRole.RESPONSABLE)
    usecase = recruteur_integration_container.get_organisme_recruteur_usecase()

    organisme = usecase.execute(
        command=GetOrganismeRecruteurQuery(
            organisme_id=organisme_model.id, utilisateur_id=agent.utilisateur_id
        )
    )
    events = organisme.collect_events()
    assert len(events) == 0
    assert organisme.entity_id == organisme_model.id


def test_initialize_organisme_steps(recruteur_integration_container):
    agent, organisme_model = _create_agent(AgentOrganismeRole.RESPONSABLE)
    usecase = recruteur_integration_container.initialize_organisme_steps_usecase()

    organisme = usecase.execute(
        command=InitializeOrganismeStepsCommand(
            organisme_id=organisme_model.id, utilisateur_id=agent.utilisateur_id
        )
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert organisme.etapes is not None
    assert len(organisme.etapes) == NB_ETAPES_PAR_DEFAUT


def test_update_organisme_steps(recruteur_integration_container):
    etapes = EtapeRecrutementFactory.create_entities()

    agent, organisme_model = _create_agent(
        AgentOrganismeRole.RESPONSABLE, etapes=etapes
    )

    nouvelles_etapes = EtapeRecrutementFactory.to_etape_data_list(etapes)

    usecase = recruteur_integration_container.update_organisme_steps_usecase()
    organisme = usecase.execute(
        command=UpdateOrganismeStepsCommand(
            utilisateur_id=agent.utilisateur_id,
            organisme_id=organisme_model.id,
            etapes=nouvelles_etapes,
        )
    )
    assert organisme.etapes is not None
    assert len(organisme.etapes) == len(nouvelles_etapes)
    usecase.audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=agent.utilisateur_id, aggregate=organisme
    )


class TestGetOrganismeRecruteurRbac:
    @pytest.mark.parametrize(
        ("role", "est_staff"),
        [(AgentOrganismeRole.RESPONSABLE, False), (None, True)],
        ids=["responsable", "staff"],
    )
    def test_role_grants_access(self, recruteur_integration_container, role, est_staff):
        agent, organisme = _create_agent(role)
        usecase = recruteur_integration_container.get_organisme_recruteur_usecase()

        result = usecase.execute(
            GetOrganismeRecruteurQuery(
                organisme_id=organisme.id,
                utilisateur_id=agent.utilisateur_id,
                est_staff=est_staff,
            )
        )

        assert result.entity_id == organisme.id

    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.MEMBRE, None], ids=["membre", "non_membre"]
    )
    def test_role_refuse_access(self, recruteur_integration_container, role):
        agent, organisme = _create_agent(role)
        usecase = recruteur_integration_container.get_organisme_recruteur_usecase()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                GetOrganismeRecruteurQuery(
                    organisme_id=organisme.id, utilisateur_id=agent.utilisateur_id
                )
            )


class TestInitializeOrganismeStepsRbac:
    @pytest.mark.parametrize(
        ("role", "est_staff"),
        [(AgentOrganismeRole.RESPONSABLE, False), (None, True)],
        ids=["responsable", "staff"],
    )
    def test_role_grants_access(self, recruteur_integration_container, role, est_staff):
        agent, organisme = _create_agent(role)
        usecase = recruteur_integration_container.initialize_organisme_steps_usecase()

        result = usecase.execute(
            InitializeOrganismeStepsCommand(
                organisme_id=organisme.id,
                utilisateur_id=agent.utilisateur_id,
                est_staff=est_staff,
            )
        )

        assert result.etapes is not None
        assert len(result.etapes) == NB_ETAPES_PAR_DEFAUT

    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.MEMBRE, None], ids=["membre", "non_membre"]
    )
    def test_role_refuse_access(self, recruteur_integration_container, role):
        agent, organisme = _create_agent(role)
        usecase = recruteur_integration_container.initialize_organisme_steps_usecase()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                InitializeOrganismeStepsCommand(
                    organisme_id=organisme.id, utilisateur_id=agent.utilisateur_id
                )
            )


class TestUpdateOrganismeStepsRbac:
    def _command(self, organisme, agent, *, est_staff=False):
        etapes = EtapeRecrutementFactory.create_entities()
        nouvelles_etapes = EtapeRecrutementFactory.to_etape_data_list(etapes)
        return UpdateOrganismeStepsCommand(
            utilisateur_id=agent.utilisateur_id,
            organisme_id=organisme.id,
            etapes=nouvelles_etapes,
            est_staff=est_staff,
        )

    @pytest.mark.parametrize(
        ("role", "est_staff"),
        [(AgentOrganismeRole.RESPONSABLE, False), (None, True)],
        ids=["responsable", "staff"],
    )
    def test_role_grants_access(self, recruteur_integration_container, role, est_staff):
        agent, organisme = _create_agent(role)
        usecase = recruteur_integration_container.update_organisme_steps_usecase()

        result = usecase.execute(self._command(organisme, agent, est_staff=est_staff))

        assert result.etapes is not None

    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.MEMBRE, None], ids=["membre", "non_membre"]
    )
    def test_role_refuse_access(self, recruteur_integration_container, role):
        agent, organisme = _create_agent(role)
        usecase = recruteur_integration_container.update_organisme_steps_usecase()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(self._command(organisme, agent))
