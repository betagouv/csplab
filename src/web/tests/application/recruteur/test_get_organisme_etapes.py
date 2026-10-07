from unittest.mock import patch
from uuid import uuid4

import pytest

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.services.get_organisme_etapes import get_organisme_etapes
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)


@patch.object(OrganismePermissionService, "can_execute")
def test_unknown_organisme_after_permission_check_raises(_can_execute, db):
    with pytest.raises(OrganismeNexistePas) as error:
        get_organisme_etapes(
            organisme_id=uuid4(), utilisateur=UtilisateurDjangoFactory()
        )

    assert isinstance(error.value.__cause__, OrganismeModel.DoesNotExist)
