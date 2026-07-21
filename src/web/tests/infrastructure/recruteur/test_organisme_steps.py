from unittest.mock import MagicMock
from uuid import uuid4

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
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from infrastructure.di.recruteur.recruteur_container import RecruteurContainer
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
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
    container.organisme_permission_service.override(
        MagicMock(spec=OrganismePermissionService)
    )
    return container


def test_get_organisme_steps(recruteur_integration_container):
    organisme_model = OrganismeFactory.create_model()
    organisme_model.save()
    usecase = recruteur_integration_container.get_organisme_recruteur_usecase()

    organisme = usecase.execute(
        command=GetOrganismeRecruteurQuery(
            organisme_id=organisme_model.id, utilisateur_id=uuid4()
        )
    )
    events = organisme.collect_events()
    assert len(events) == 0
    assert organisme.entity_id == organisme_model.id


def test_initialize_organisme_steps(recruteur_integration_container):
    organisme_model = OrganismeFactory.create_model()
    usecase = recruteur_integration_container.initialize_organisme_steps_usecase()

    organisme = usecase.execute(
        command=InitializeOrganismeStepsCommand(
            organisme_id=organisme_model.id, utilisateur_id=uuid4()
        )
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert organisme.etapes is not None
    assert len(organisme.etapes) == NB_ETAPES_PAR_DEFAUT


def test_update_organisme_steps(recruteur_integration_container):
    etapes = EtapeRecrutementFactory.create_entities()

    organisme_model = OrganismeFactory.create_model(etapes=etapes)

    nouvelles_etapes = EtapeRecrutementFactory.to_etape_data_list(etapes)

    utilisateur_id = uuid4()
    usecase = recruteur_integration_container.update_organisme_steps_usecase()
    organisme = usecase.execute(
        command=UpdateOrganismeStepsCommand(
            utilisateur_id=utilisateur_id,
            organisme_id=organisme_model.id,
            etapes=nouvelles_etapes,
        )
    )
    assert organisme.etapes is not None
    assert len(organisme.etapes) == len(nouvelles_etapes)
    usecase.audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=utilisateur_id, aggregate=organisme
    )
