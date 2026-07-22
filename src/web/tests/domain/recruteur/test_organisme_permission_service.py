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

RESPONSABLE_ACTIONS = [
    OrganismeAction.GET_ORGANISME,
    OrganismeAction.INITIALIZE_ORGANISME_STEPS,
    OrganismeAction.UPDATE_ORGANISME_STEPS,
]
RESPONSABLE_AND_MEMBRE_ACTIONS = [
    OrganismeAction.LISTER_MES_RECRUTEMENTS,
    OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
]
STAFF_BYPASS_ACTIONS = [
    OrganismeAction.GET_ORGANISME,
    OrganismeAction.INITIALIZE_ORGANISME_STEPS,
    OrganismeAction.UPDATE_ORGANISME_STEPS,
]


def _service(
    role: AgentOrganismeRole | None,
) -> tuple[OrganismePermissionService, Mock]:
    repository = Mock(spec=IOrganismeAgentRepository)
    repository.get_role.return_value = role
    return OrganismePermissionService(organisme_agent_repository=repository), repository


class TestEstAutorise:
    @pytest.mark.parametrize("action", RESPONSABLE_ACTIONS)
    def test_responsable_only_actions_allow_responsable(
        self, action: OrganismeAction
    ) -> None:
        service, repository = _service(AgentOrganismeRole.RESPONSABLE)
        organisme_id, agent_id = uuid4(), uuid4()

        result = service.est_autorise(
            action=action,
            organisme_id=organisme_id,
            agent_id=agent_id,
            est_staff=False,
        )

        assert result == AgentOrganismeRole.RESPONSABLE
        repository.get_role.assert_called_once_with(
            organisme_id=organisme_id, agent_id=agent_id
        )

    @pytest.mark.parametrize("action", RESPONSABLE_ACTIONS)
    @pytest.mark.parametrize("role", [AgentOrganismeRole.MEMBRE, None])
    def test_responsable_only_actions_reject_non_responsable(
        self, action: OrganismeAction, role: AgentOrganismeRole | None
    ) -> None:
        service, _ = _service(role)

        with pytest.raises(AccesOrganismeRefuse):
            service.est_autorise(
                action=action, organisme_id=uuid4(), agent_id=uuid4(), est_staff=False
            )

    @pytest.mark.parametrize("action", RESPONSABLE_AND_MEMBRE_ACTIONS)
    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE]
    )
    def test_shared_actions_allow_responsable_and_membre(
        self, action: OrganismeAction, role: AgentOrganismeRole
    ) -> None:
        service, _ = _service(role)

        result = service.est_autorise(
            action=action, organisme_id=uuid4(), agent_id=uuid4(), est_staff=False
        )

        assert result == role

    @pytest.mark.parametrize("action", RESPONSABLE_AND_MEMBRE_ACTIONS)
    def test_shared_actions_reject_no_role(self, action: OrganismeAction) -> None:
        service, _ = _service(None)

        with pytest.raises(AccesOrganismeRefuse):
            service.est_autorise(
                action=action, organisme_id=uuid4(), agent_id=uuid4(), est_staff=False
            )


class TestStaffBypass:
    @pytest.mark.parametrize("action", STAFF_BYPASS_ACTIONS)
    def test_staff_bypasses_role_check(self, action: OrganismeAction) -> None:
        service, repository = _service(None)

        result = service.est_autorise(
            action=action, organisme_id=uuid4(), agent_id=uuid4(), est_staff=True
        )

        assert result is None
        repository.get_role.assert_not_called()

    @pytest.mark.parametrize(
        "action", [a for a in OrganismeAction if a not in STAFF_BYPASS_ACTIONS]
    )
    def test_staff_does_not_bypass_for_other_actions(
        self, action: OrganismeAction
    ) -> None:
        service, repository = _service(None)

        with pytest.raises(AccesOrganismeRefuse):
            service.est_autorise(
                action=action, organisme_id=uuid4(), agent_id=uuid4(), est_staff=True
            )

        repository.get_role.assert_called_once()
