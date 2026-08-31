from typing import cast
from unittest.mock import Mock

import pytest
from referentiel.events.organisme_events import OrganismeModifie
from referentiel.value_objects.verse import Verse

from application.identite.usecases.update_organisme import (
    UpdateOrganismeCommand,
    UpdateOrganismeUsecase,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from domain.identite.repositories.organisme_repository_interface import (
    IOrganismeRepository,
)
from domain.identite.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentRecrutementRole
from infrastructure.factories.identite.organisme_factory import OrganismeFactory
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from tests.utils.interface_aware_mock import create_interface_aware_mock


@pytest.fixture(name="permission_service")
def permission_service_fixture():
    service = Mock(spec=OrganismePermissionService)
    service.est_autorise.return_value = AgentRecrutementRole.RESPONSABLE
    return service


@pytest.fixture(name="organisme")
def organisme_fixture():
    return OrganismeFactory.create_entity()


@pytest.fixture(name="organisme_repository")
def organisme_repository_fixture(organisme):
    repo = Mock(spec=IOrganismeRepository)
    repo = cast(IOrganismeRepository, create_interface_aware_mock(IOrganismeRepository))
    repo.create(organisme)
    return repo


@pytest.fixture(name="audit_log_writer")
def audit_log_writer_fixture():
    return Mock(spec=AuditLogWriter)


@pytest.fixture(name="usecase")
def usecase_fixture(
    permission_service,
    organisme_repository,
    audit_log_writer,
):
    return UpdateOrganismeUsecase(
        organisme_repository=organisme_repository,
        permission_service=permission_service,
        audit_log_writer=audit_log_writer,
    )


def test_update_organisme_success(
    permission_service, audit_log_writer, organisme, usecase
):
    utilisateur = UtilisateurFactory.create_entity(is_staff=True)
    command = UpdateOrganismeCommand(
        organisme_id=organisme.entity_id,
        name="Commune de Paris",
        verse=Verse.FPT,
        managed_ats=True,
        utilisateur=utilisateur,
    )

    result = usecase.execute(command)
    permission_service.est_autorise.assert_called_once_with(
        action=OrganismeAction.MODIFIER_ORGANISME,
        utilisateur=utilisateur,
    )
    audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=utilisateur.entity_id, aggregate=organisme
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeModifie)
    assert result.entity_id == organisme.entity_id
    assert result.nom == command.name
    assert result.versant == command.verse
    assert result.gestion_ats == command.managed_ats


def test_update_organisme_refuse_non_staff(permission_service, organisme, usecase):
    command = UpdateOrganismeCommand(
        organisme_id=organisme.entity_id,
        name="Commune de Paris",
        verse=Verse.FPT,
        managed_ats=True,
        utilisateur=UtilisateurFactory.create_entity(is_staff=False),
    )
    permission_service.est_autorise.side_effect = OperationOrganismeRefusee()

    with pytest.raises(OperationOrganismeRefusee):
        usecase.execute(command=command)
