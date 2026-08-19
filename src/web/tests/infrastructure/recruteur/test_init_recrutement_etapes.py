from unittest.mock import Mock
from uuid import UUID, uuid4

import pytest

from application.recruteur.usecases.init_recrutement_etapes import (
    InitRecrutementEtapesCommand,
)
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.recruteur.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory
from infrastructure.gateways.shared.logger import LoggerService

NB_ETAPES_PAR_DEFAUT = 6


@pytest.fixture(name="recruteur_integration_container")
def recruteur_integration_container_fixture(db):
    container = RecruteurContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(Mock(spec=AuditLogWriter))
    return container


class TestInitRecrutementEtapes:
    @pytest.mark.parametrize(
        "kwargs",
        [
            {"organisme_role": AgentOrganismeRole.RESPONSABLE},
            {
                "organisme_role": AgentOrganismeRole.MEMBRE,
                "agent_role": AgentRecrutementRole.RESPONSABLE,
            },
        ],
        ids=["responsable_organisme", "responsable_recrutement"],
    )
    def test_init_recrutement_etapes(self, db, recruteur_integration_container, kwargs):
        # parametres par defaut = une seule etape en cours
        en_cours = EtapeRecrutementFactory.create_entity()
        etapes = EtapeRecrutementFactory.create_entity_batch(en_cours=(en_cours,))

        agent, organisme = OrganismeFactory.create_model_with_agent(
            role=kwargs.get("organisme_role"), etapes=etapes
        )
        recrutement_model = RecrutementFactory.create_model(
            organisme_id=organisme.id,
            agent_id=UUID(agent.utilisateur_id),
            agent_role=kwargs.get("agent_role"),
            persist_etapes=False,
        )
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        resultat = usecase.execute(
            InitRecrutementEtapesCommand(
                organisme_id=recrutement_model.organisme_id,
                recrutement_id=recrutement_model.offre_id,
                utilisateur_id=UUID(agent.utilisateur_id),
            )
        )

        assert resultat == etapes

    @pytest.mark.parametrize(
        "agent_role",
        [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR],
    )
    def test_denied_agents(self, db, recruteur_integration_container, agent_role):
        recrutement_model = RecrutementFactory.create_model(agent_role=agent_role)
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        with pytest.raises(AccesRecrutementRefuse):
            usecase.execute(
                InitRecrutementEtapesCommand(
                    organisme_id=recrutement_model.organisme_id,
                    recrutement_id=recrutement_model.offre_id,
                    utilisateur_id=recrutement_model.agents_liaisons.get().agent_id,
                )
            )

    def test_agents_without_role(self, db, recruteur_integration_container):
        recrutement_model = RecrutementFactory.create_model()
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        with pytest.raises(AccesOrganismeRefuse):
            usecase.execute(
                InitRecrutementEtapesCommand(
                    organisme_id=recrutement_model.organisme_id,
                    recrutement_id=recrutement_model.offre_id,
                    utilisateur_id=uuid4(),
                )
            )
