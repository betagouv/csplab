from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.recruteur.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.services.organisme_permission_service import (
    OrganismePermissionService,
)
from domain.recruteur.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import AgentOrganismeRole


def test_est_autorise_passes_when_agent_is_responsable() -> None:
    organisme_id = uuid4()
    agent_id = uuid4()
    repository = Mock(spec=IOrganismeAgentRepository)
    repository.get_role.return_value = AgentOrganismeRole.RESPONSABLE
    service = OrganismePermissionService(organisme_agent_repository=repository)

    result = service.est_autorise(
        action=OrganismeAction.GET_ORGANISME,
        organisme_id=organisme_id,
        agent_id=agent_id,
        est_staff=False,
    )

    assert result == AgentOrganismeRole.RESPONSABLE
    repository.get_role.assert_called_once_with(
        organisme_id=organisme_id, agent_id=agent_id
    )


def test_est_autorise_raises_when_agent_is_membre() -> None:
    repository = Mock(spec=IOrganismeAgentRepository)
    repository.get_role.return_value = AgentOrganismeRole.MEMBRE
    service = OrganismePermissionService(organisme_agent_repository=repository)

    with pytest.raises(AccesOrganismeRefuse):
        service.est_autorise(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=uuid4(),
            agent_id=uuid4(),
            est_staff=False,
        )


def test_est_autorise_raises_when_agent_has_no_role() -> None:
    repository = Mock(spec=IOrganismeAgentRepository)
    repository.get_role.return_value = None
    service = OrganismePermissionService(organisme_agent_repository=repository)

    with pytest.raises(AccesOrganismeRefuse):
        service.est_autorise(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=uuid4(),
            agent_id=uuid4(),
            est_staff=False,
        )


def test_verifier_responsable_passes_when_staff_even_if_not_responsable() -> None:
    repository = Mock(spec=IOrganismeAgentRepository)
    service = OrganismePermissionService(organisme_agent_repository=repository)

    service.est_autorise(
        action=OrganismeAction.GET_ORGANISME,
        organisme_id=uuid4(),
        agent_id=uuid4(),
        est_staff=True,
    )

    repository.get_role.assert_not_called()


@pytest.mark.parametrize(
    "action",
    [a for a in OrganismeAction if a != OrganismeAction.LISTER_MES_RECRUTEMENTS],
)
def test_every_organisme_action_currently_requires_responsable(
    action: OrganismeAction,
) -> None:
    repository = Mock(spec=IOrganismeAgentRepository)
    repository.get_role.return_value = AgentOrganismeRole.MEMBRE
    service = OrganismePermissionService(organisme_agent_repository=repository)

    with pytest.raises(AccesOrganismeRefuse):
        service.est_autorise(
            action=action,
            organisme_id=uuid4(),
            agent_id=uuid4(),
            est_staff=False,
        )


def test_lister_mes_recrutements_allows_responsable() -> None:
    repository = Mock(spec=IOrganismeAgentRepository)
    repository.get_role.return_value = AgentOrganismeRole.RESPONSABLE
    service = OrganismePermissionService(organisme_agent_repository=repository)

    result = service.est_autorise(
        action=OrganismeAction.LISTER_MES_RECRUTEMENTS,
        organisme_id=uuid4(),
        agent_id=uuid4(),
        est_staff=False,
    )

    assert result == AgentOrganismeRole.RESPONSABLE


def test_lister_mes_recrutements_allows_membre() -> None:
    repository = Mock(spec=IOrganismeAgentRepository)
    repository.get_role.return_value = AgentOrganismeRole.MEMBRE
    service = OrganismePermissionService(organisme_agent_repository=repository)

    result = service.est_autorise(
        action=OrganismeAction.LISTER_MES_RECRUTEMENTS,
        organisme_id=uuid4(),
        agent_id=uuid4(),
        est_staff=False,
    )

    assert result == AgentOrganismeRole.MEMBRE


def test_lister_mes_recrutements_raises_when_no_role() -> None:
    repository = Mock(spec=IOrganismeAgentRepository)
    repository.get_role.return_value = None
    service = OrganismePermissionService(organisme_agent_repository=repository)

    with pytest.raises(AccesOrganismeRefuse):
        service.est_autorise(
            action=OrganismeAction.LISTER_MES_RECRUTEMENTS,
            organisme_id=uuid4(),
            agent_id=uuid4(),
            est_staff=False,
        )
