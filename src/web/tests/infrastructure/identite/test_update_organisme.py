from unittest.mock import Mock

import pytest
from referentiel.value_objects.verse import Verse

from application.identite.usecases.update_organisme import (
    UpdateOrganismeCommand,
)
from config.app_config import AppConfig
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from infrastructure.di.identite.identite_container import IdentiteContainer
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.gateways.shared.logger import LoggerService


@pytest.fixture(name="organisme")
def organisme_fixture():
    return OrganismeFactory.create_model()


@pytest.fixture(name="identite_integration_container")
def identite_integration_container_fixture(db):
    container = IdentiteContainer()
    app_config = AppConfig.from_django_settings()
    logger_service = LoggerService()
    container.app_config.override(app_config)
    container.logger_service.override(logger_service)
    container.audit_log_writer.override(Mock(spec=AuditLogWriter))
    return container


def test_update_organisme(db, organisme, identite_integration_container):
    command = UpdateOrganismeCommand(
        organisme_id=organisme.id,
        name="Commune de Paris",
        verse=Verse.FPT,
        managed_ats=True,
        utilisateur=UtilisateurFactory.create_entity(is_staff=True),
    )

    result = identite_integration_container.update_organisme_usecase().execute(command)

    assert result.entity_id == command.organisme_id
    assert result.nom == command.name
    assert result.versant == command.verse
    assert result.gestion_ats == command.managed_ats


def test_update_organisme_refuse_non_staff(
    db, organisme, identite_integration_container
):
    command = UpdateOrganismeCommand(
        organisme_id=organisme.id,
        name="Commune de Paris",
        verse=Verse.FPT,
        managed_ats=True,
        utilisateur=UtilisateurFactory.create_entity(is_staff=False),
    )

    with pytest.raises(OperationOrganismeRefusee):
        identite_integration_container.update_organisme_usecase().execute(command)
