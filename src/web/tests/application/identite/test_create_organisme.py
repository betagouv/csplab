from typing import cast
from unittest.mock import Mock

import pytest
from referentiel.events.organisme_events import OrganismeCree
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from application.identite.usecases.create_organisme import (
    CreateOrganismeCommand,
    CreateOrganismeUsecase,
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
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from tests.utils.interface_aware_mock import create_interface_aware_mock


@pytest.fixture(name="permission_service")
def permission_service_fixture():
    service = Mock(spec=OrganismePermissionService)
    service.est_autorise.return_value = AgentRecrutementRole.RESPONSABLE
    return service


@pytest.fixture(name="organisme_repository")
def organisme_repository_fixture():
    repo = Mock(spec=IOrganismeRepository)
    repo = cast(IOrganismeRepository, create_interface_aware_mock(IOrganismeRepository))
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
    return CreateOrganismeUsecase(
        organisme_repository=organisme_repository,
        permission_service=permission_service,
        audit_log_writer=audit_log_writer,
    )


def test_create_organisme_success(permission_service, audit_log_writer, usecase):
    utilisateur = UtilisateurFactory.create_entity(is_staff=True)
    command = CreateOrganismeCommand(
        name="Commune de Paris",
        verse=Verse.FPT,
        localisation=None,
        siret=SIRET(code="26060047300342"),
        parent_id=None,
        utilisateur=utilisateur,
    )

    organisme = usecase.execute(command=command)
    permission_service.est_autorise.assert_called_once_with(
        action=OrganismeAction.CREER_ORGANISME,
        utilisateur=utilisateur,
    )
    audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=utilisateur.entity_id, aggregate=organisme
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeCree)
    assert organisme.nom == "Commune de Paris"
    assert organisme.versant == Verse.FPT


def test_create_organisme_refuse_non_staff(permission_service, usecase):
    command = CreateOrganismeCommand(
        name="Commune de Paris",
        verse=Verse.FPT,
        localisation=None,
        siret=SIRET(code="26060047300342"),
        parent_id=None,
        utilisateur=UtilisateurFactory.create_entity(is_staff=False),
    )
    permission_service.est_autorise.side_effect = OperationOrganismeRefusee()

    with pytest.raises(OperationOrganismeRefusee):
        usecase.execute(command=command)
