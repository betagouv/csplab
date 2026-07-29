from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.usecases.init_recrutement_etapes import (
    InitRecrutementEtapesCommand,
)
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from domain.recruteur.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
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
    container.audit_log_writer.override(MagicMock(spec=AuditLogWriter))
    return container


# TODO : update this class after persistence is implemented
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
        recrutement_model = RecrutementFactory.create_model(**kwargs)
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        resultat = usecase.execute(
            InitRecrutementEtapesCommand(
                organisme_id=recrutement_model.organisme_id,
                recrutement_id=recrutement_model.offre_id,
                utilisateur_id=recrutement_model.agents_liaisons.get().agent_id,
            )
        )

        assert len(resultat) == NB_ETAPES_PAR_DEFAUT

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

    def test_init_recrutement_etapes_raises_when_organisme_introuvable(
        self, db, recruteur_integration_container
    ):
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        with pytest.raises(OrganismeNexistePas):
            usecase.execute(
                InitRecrutementEtapesCommand(
                    organisme_id=uuid4(),
                    recrutement_id=uuid4(),
                    utilisateur_id=uuid4(),
                )
            )
