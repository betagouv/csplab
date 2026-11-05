from unittest.mock import Mock, patch
from uuid import uuid4

import pytest
from referentiel.value_objects.verse import Verse

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.services.update_organisme import update_organisme
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.commons.services.audit_log_writer import AuditLogWriter
from domain.identite.errors.organisme_permission_errors import (
    OperationOrganismeRefusee,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)

pytestmark = pytest.mark.django_db


def _update(organisme_id, utilisateur):
    return update_organisme(
        organisme_id=organisme_id,
        utilisateur=utilisateur,
        nom="Commune de Paris",
        versant=Verse.FPT,
        gestion_ats=True,
    )


@patch.object(
    OrganismePermissionService, "can_execute", side_effect=OperationOrganismeRefusee()
)
def test_checks_permission_before_writing(can_execute):
    organisme = OrganismeDjangoFactory()
    utilisateur = UtilisateurDjangoFactory(is_staff=False)

    with pytest.raises(OperationOrganismeRefusee):
        _update(organisme.id, utilisateur)

    can_execute.assert_called_once_with(
        action=OrganismeAction.UPDATE_ORGANISME,
        utilisateur=utilisateur,
        organisme_id=organisme.id,
    )
    assert OrganismeModel.objects.get(pk=organisme.id).nom == organisme.nom
    assert not AuditLogModel.objects.exists()


@patch.object(OrganismePermissionService, "can_execute", new=Mock())
def test_raises_when_organisme_disappears_after_permission_check():
    organisme_id = uuid4()

    with pytest.raises(OrganismeNexistePas) as raised:
        _update(organisme_id, UtilisateurDjangoFactory(is_staff=True))

    assert raised.value.identifier == str(organisme_id)
    assert not AuditLogModel.objects.exists()


@patch.object(AuditLogWriter, "log_action", new=Mock(side_effect=RuntimeError("audit")))
def test_rolls_back_the_update_when_the_audit_log_fails():
    organisme = OrganismeDjangoFactory(gestion_ats=False)

    with pytest.raises(RuntimeError):
        _update(organisme.id, UtilisateurDjangoFactory(is_staff=True))

    persisted = OrganismeModel.objects.get(pk=organisme.id)
    assert persisted.nom == organisme.nom
    assert persisted.gestion_ats is False
