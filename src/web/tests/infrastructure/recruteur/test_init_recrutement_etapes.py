from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from application.recruteur.usecases.init_recrutement_etapes import (
    InitRecrutementEtapesCommand,
)
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_errors import OrganismeNexistePas
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
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


class TestInitRecrutementEtapes:
    # TODO : update this class after persistence is implemented
    def test_init_recrutement_etapes(self, db, recruteur_integration_container):
        organisme_model = OrganismeFactory.create_model()
        usecase = recruteur_integration_container.init_recrutement_etapes_usecase()

        resultat = usecase.execute(
            InitRecrutementEtapesCommand(
                organisme_id=organisme_model.id,
                recrutement_id=uuid4(),
                utilisateur_id=uuid4(),
            )
        )

        assert len(resultat) == NB_ETAPES_PAR_DEFAUT

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
