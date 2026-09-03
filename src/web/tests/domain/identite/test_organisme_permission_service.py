from unittest.mock import Mock
from uuid import uuid4

import pytest

from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.identite.services.organisme_permission_service import (
    _ROLES_RECRUTEMENT_REQUIS,
    _ROLES_REQUIS,
    _SANS_ROLE_RECRUTEMENT_REQUIS,
    OrganismePermissionService,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.repositories.organisme_agent_repository_interface import (
    IOrganismeAgentRepository,
)
from domain.recruteur.repositories.organisme_repository_interface import (
    IOrganismeRecruteurRepository,
)
from domain.recruteur.repositories.recrutement_agent_repository_interface import (
    IRecrutementAgentRepository,
)
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory

# TODO: add test for CHANGER_ETAPE_CANDIDATURES

RESPONSABLE_ACTIONS = [
    OrganismeAction.GET_ORGANISME,
    OrganismeAction.INITIALIZE_ORGANISME_STEPS,
    OrganismeAction.UPDATE_ORGANISME_STEPS,
    OrganismeAction.LIST_ORGANISME_AGENTS,
    OrganismeAction.ATTACH_ORGANISME_AGENT,
    OrganismeAction.UPDATE_ORGANISME_AGENT,
    OrganismeAction.REVOKE_ORGANISME_AGENT,
    OrganismeAction.CREATE_AGENT,
]
STAFF_BYPASS_ACTIONS = [
    OrganismeAction.GET_ORGANISME,
    OrganismeAction.INITIALIZE_ORGANISME_STEPS,
    OrganismeAction.UPDATE_ORGANISME_STEPS,
    OrganismeAction.LIST_ORGANISME_AGENTS,
    OrganismeAction.ATTACH_ORGANISME_AGENT,
    OrganismeAction.UPDATE_ORGANISME_AGENT,
    OrganismeAction.REVOKE_ORGANISME_AGENT,
    OrganismeAction.CREATE_AGENT,
]


def _service(
    role: AgentOrganismeRole | None,
    recrutement_role: AgentRecrutementRole | None = None,
    organisme_recruteur_repository: Mock | None = None,
) -> tuple[OrganismePermissionService, Mock, Mock]:
    if organisme_recruteur_repository is None:
        organisme_recruteur_repository = Mock(spec=IOrganismeRecruteurRepository)
    repository = Mock(spec=IOrganismeAgentRepository)
    repository.get_role.return_value = role
    recrutement_repository = Mock(spec=IRecrutementAgentRepository)
    recrutement_repository.get_role.return_value = recrutement_role
    service = OrganismePermissionService(
        organisme_recruteur_repository=organisme_recruteur_repository,
        organisme_agent_repository=repository,
        recrutement_agent_repository=recrutement_repository,
    )
    return service, repository, recrutement_repository


@pytest.mark.parametrize("action", RESPONSABLE_ACTIONS)
class TestResponsableActions:
    def test_responsable_actions_allow_responsable(
        self, action: OrganismeAction
    ) -> None:
        service, repository, _ = _service(AgentOrganismeRole.RESPONSABLE)
        organisme_id, agent_id = uuid4(), uuid4()

        result = service.est_autorise(
            action=action,
            organisme_id=organisme_id,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=agent_id, is_staff=False
            ),
        )

        assert result == AgentOrganismeRole.RESPONSABLE
        repository.get_role.assert_called_once_with(
            organisme_id=organisme_id, agent_id=agent_id
        )

    def test_staff_bypasses_role_check(self, action: OrganismeAction) -> None:
        service, repository, _ = _service(None)

        result = service.est_autorise(
            action=action,
            organisme_id=uuid4(),
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=uuid4(), is_staff=True
            ),
        )

        assert result is None
        repository.get_role.assert_not_called()

    @pytest.mark.parametrize("role", [AgentOrganismeRole.MEMBRE, None])
    def test_responsable_actions_reject_non_responsable(
        self, action: OrganismeAction, role: AgentOrganismeRole | None
    ) -> None:
        service, _, _ = _service(role)

        with pytest.raises(AccesOrganismeRefuse):
            service.est_autorise(
                action=action,
                organisme_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=False
                ),
            )


class TestListerMesRecrutementRbac:
    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE]
    )
    def test_allow_responsable_and_membre(self, role: AgentOrganismeRole) -> None:
        service, _, _ = _service(role)

        result = service.est_autorise(
            action=OrganismeAction.LISTER_MES_RECRUTEMENTS,
            organisme_id=uuid4(),
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=uuid4(), is_staff=False
            ),
        )

        assert result == role

    @pytest.mark.parametrize("est_staff", [False, True])
    def test_reject_no_role_nor_staff(self, est_staff: bool) -> None:
        service, _, _ = _service(None)

        with pytest.raises(AccesOrganismeRefuse):
            service.est_autorise(
                action=OrganismeAction.LISTER_MES_RECRUTEMENTS,
                organisme_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=est_staff
                ),
            )


class TestVoirDetailRecrutementRbac:
    @pytest.mark.parametrize("recrutement_role", list(AgentRecrutementRole))
    def test_membre_with_recrutement_role_is_allowed(
        self, recrutement_role: AgentRecrutementRole
    ) -> None:
        service, _, recrutement_repository = _service(
            AgentOrganismeRole.MEMBRE, recrutement_role
        )
        organisme_id, agent_id, recrutement_id = uuid4(), uuid4(), uuid4()

        result = service.est_autorise(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=organisme_id,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=agent_id, is_staff=False
            ),
            recrutement_id=recrutement_id,
        )

        assert result == AgentOrganismeRole.MEMBRE
        recrutement_repository.get_role.assert_called_once_with(
            recrutement_id=recrutement_id, agent_id=agent_id
        )

    def test_responsable_bypasses_recrutement_check(self) -> None:
        service, _, recrutement_repository = _service(
            AgentOrganismeRole.RESPONSABLE, None
        )

        result = service.est_autorise(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=uuid4(),
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=uuid4(), is_staff=False
            ),
            recrutement_id=uuid4(),
        )

        assert result == AgentOrganismeRole.RESPONSABLE
        recrutement_repository.get_role.assert_not_called()

    def test_membre_without_recrutement_role_is_denied(self) -> None:
        service, _, _ = _service(AgentOrganismeRole.MEMBRE, None)

        with pytest.raises(AccesRecrutementRefuse):
            service.est_autorise(
                action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
                organisme_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=False
                ),
                recrutement_id=uuid4(),
            )

    def test_unprovided_recrutement_id_is_denied(self) -> None:
        service, _, recrutement_repository = _service(AgentOrganismeRole.MEMBRE, None)

        with pytest.raises(AccesRecrutementInconnu):
            service.est_autorise(
                action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
                organisme_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=False
                ),
            )

    def test_staff_without_role_is_denied(self) -> None:
        service, _, _ = _service(AgentOrganismeRole.MEMBRE, None)

        with pytest.raises(AccesRecrutementRefuse):
            service.est_autorise(
                action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
                organisme_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=True
                ),
                recrutement_id=uuid4(),
            )


RECRUTEMENT_ETAPES_ACTIONS = [
    OrganismeAction.GET_RECRUTEMENT_ETAPES,
    OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
    OrganismeAction.INIT_RECRUTEMENT_ETAPES,
]


@pytest.mark.parametrize("action", RECRUTEMENT_ETAPES_ACTIONS)
class TestRecrutementEtapesRbac:
    def test_organisme_responsable_bypasses_recrutement_check(
        self, action: OrganismeAction
    ) -> None:
        service, _, recrutement_repository = _service(
            AgentOrganismeRole.RESPONSABLE, None
        )

        result = service.est_autorise(
            action=action,
            organisme_id=uuid4(),
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=uuid4(), is_staff=False
            ),
            recrutement_id=uuid4(),
        )

        assert result == AgentOrganismeRole.RESPONSABLE
        recrutement_repository.get_role.assert_not_called()

    def test_membre_with_recrutement_responsable_is_allowed(
        self, action: OrganismeAction
    ) -> None:
        service, _, recrutement_repository = _service(
            AgentOrganismeRole.MEMBRE, AgentRecrutementRole.RESPONSABLE
        )
        organisme_id, agent_id, recrutement_id = uuid4(), uuid4(), uuid4()

        result = service.est_autorise(
            action=action,
            organisme_id=organisme_id,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=agent_id, is_staff=False
            ),
            recrutement_id=recrutement_id,
        )

        assert result == AgentOrganismeRole.MEMBRE
        recrutement_repository.get_role.assert_called_once_with(
            recrutement_id=recrutement_id, agent_id=agent_id
        )

    @pytest.mark.parametrize(
        "recrutement_role",
        [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR, None],
    )
    def test_membre_without_recrutement_responsable_is_denied(
        self, action: OrganismeAction, recrutement_role: AgentRecrutementRole
    ) -> None:
        service, _, _ = _service(AgentOrganismeRole.MEMBRE, recrutement_role)

        with pytest.raises(AccesRecrutementRefuse):
            service.est_autorise(
                action=action,
                organisme_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=False
                ),
                recrutement_id=uuid4(),
            )

    def test_unprovided_recrutement_id_is_denied(self, action: OrganismeAction) -> None:
        service, _, recrutement_repository = _service(AgentOrganismeRole.MEMBRE, None)

        with pytest.raises(AccesRecrutementInconnu):
            service.est_autorise(
                action=action,
                organisme_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=False
                ),
            )
        recrutement_repository.get_role.assert_not_called()

    def test_staff_without_organisme_role_is_denied(
        self, action: OrganismeAction
    ) -> None:
        service, _, _ = _service(None)

        with pytest.raises(AccesOrganismeRefuse):
            service.est_autorise(
                action=action,
                organisme_id=uuid4(),
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=True
                ),
                recrutement_id=uuid4(),
            )


def test_raises_when_organisme_not_found() -> None:
    organisme_id = uuid4()
    organisme_recruteur_repository = Mock(spec=IOrganismeRecruteurRepository)
    organisme_recruteur_repository.get_by_id.side_effect = OrganismeNexistePas(
        str(organisme_id)
    )
    service, _, _ = _service(
        AgentOrganismeRole.RESPONSABLE,
        organisme_recruteur_repository=organisme_recruteur_repository,
    )

    with pytest.raises(OrganismeNexistePas):
        service.est_autorise(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=organisme_id,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=uuid4(), is_staff=False
            ),
        )


def test_organisme_guard_runs_before_staff_bypass_and_role_check() -> None:
    organisme_id = uuid4()
    organisme_recruteur_repository = Mock(spec=IOrganismeRecruteurRepository)
    organisme_recruteur_repository.get_by_id.side_effect = OrganismeNexistePas(
        str(organisme_id)
    )
    service, repository, _ = _service(
        None, organisme_recruteur_repository=organisme_recruteur_repository
    )

    with pytest.raises(OrganismeNexistePas):
        service.est_autorise(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=organisme_id,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=uuid4(), is_staff=True
            ),
        )
    repository.get_role.assert_not_called()


def test_toute_action_membre_est_classee() -> None:
    actions_membre = frozenset(
        action
        for action, roles in _ROLES_REQUIS.items()
        if AgentOrganismeRole.MEMBRE in roles
    )

    assert actions_membre <= (
        _ROLES_RECRUTEMENT_REQUIS.keys() | _SANS_ROLE_RECRUTEMENT_REQUIS
    )


ACTIONS_SANS_ORGANISME = [
    OrganismeAction.CREER_ORGANISME,
    OrganismeAction.LISTER_ORGANISMES,
]


@pytest.mark.parametrize("action", ACTIONS_SANS_ORGANISME)
def test_staff_est_autorise_sans_appel_repository(action: OrganismeAction) -> None:
    service, repository, _ = _service(None)
    organisme_recruteur_repository = Mock(spec=IOrganismeRecruteurRepository)
    service = OrganismePermissionService(
        organisme_recruteur_repository=organisme_recruteur_repository,
        organisme_agent_repository=repository,
        recrutement_agent_repository=Mock(spec=IRecrutementAgentRepository),
    )

    result = service.est_autorise(
        action=action,
        utilisateur=UtilisateurFactory.create_entity(entity_id=uuid4(), is_staff=True),
    )

    assert result is None
    organisme_recruteur_repository.get_by_id.assert_not_called()
    repository.get_role.assert_not_called()


class TestModifierOrganisme:
    def test_staff_est_autorise(self) -> None:
        service, repository, _ = _service(None)
        organisme_id = uuid4()

        result = service.est_autorise(
            action=OrganismeAction.MODIFIER_ORGANISME,
            organisme_id=organisme_id,
            utilisateur=UtilisateurFactory.create_entity(
                entity_id=uuid4(), is_staff=True
            ),
        )

        assert result is None
        repository.get_role.assert_not_called()

    def test_non_staff_est_refuse_apres_verification_existence(self) -> None:
        organisme_id = uuid4()
        organisme_recruteur_repository = Mock(spec=IOrganismeRecruteurRepository)
        service, repository, _ = _service(
            None, organisme_recruteur_repository=organisme_recruteur_repository
        )

        with pytest.raises(OperationOrganismeRefusee):
            service.est_autorise(
                action=OrganismeAction.MODIFIER_ORGANISME,
                organisme_id=organisme_id,
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=False
                ),
            )

        organisme_recruteur_repository.get_by_id.assert_called_once_with(organisme_id)
        repository.get_role.assert_not_called()

    def test_organisme_inexistant_est_priorise_sur_le_statut_staff(self) -> None:
        organisme_id = uuid4()
        organisme_recruteur_repository = Mock(spec=IOrganismeRecruteurRepository)
        organisme_recruteur_repository.get_by_id.side_effect = OrganismeNexistePas(
            str(organisme_id)
        )
        service, _, _ = _service(
            None, organisme_recruteur_repository=organisme_recruteur_repository
        )

        with pytest.raises(OrganismeNexistePas):
            service.est_autorise(
                action=OrganismeAction.MODIFIER_ORGANISME,
                organisme_id=organisme_id,
                utilisateur=UtilisateurFactory.create_entity(
                    entity_id=uuid4(), is_staff=True
                ),
            )
