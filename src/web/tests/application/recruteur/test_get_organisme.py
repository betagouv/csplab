from unittest.mock import patch
from uuid import uuid4

import pytest

from application.identite.context_services.organisme_permission_service import (
    OrganismePermissionService,
)
from application.recruteur.services.get_organisme import get_organisme
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)

pytestmark = pytest.mark.django_db


def test_checks_permission_before_reading():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    utilisateur = agent.utilisateur

    with patch.object(
        OrganismePermissionService,
        "can_execute",
        side_effect=AccesOrganismeRefuse(organisme.id),
    ) as can_execute:
        with pytest.raises(AccesOrganismeRefuse):
            get_organisme(organisme_id=organisme.id, utilisateur=utilisateur)

    can_execute.assert_called_once_with(
        action=OrganismeAction.GET_ORGANISME,
        utilisateur=utilisateur,
        organisme_id=organisme.id,
    )


def test_raises_when_organisme_disappears_after_permission_check():
    agent, _ = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    organisme_id = uuid4()

    with patch.object(OrganismePermissionService, "can_execute"):
        with pytest.raises(OrganismeNexistePas) as raised:
            get_organisme(organisme_id=organisme_id, utilisateur=agent.utilisateur)

    assert raised.value.identifier == str(organisme_id)
