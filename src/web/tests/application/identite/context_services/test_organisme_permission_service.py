from collections.abc import Callable
from uuid import UUID, uuid4

import pytest
from django.utils import timezone

from application.identite.context_services.organisme_permission_service import (
    _RESPONSABLE_D_UN_RECRUTEMENT_REQUIS,
    _ROLES_RECRUTEMENT_REQUIS,
    _ROLES_REQUIS,
    _SANS_ROLE_RECRUTEMENT_REQUIS,
    OrganismePermissionService,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.entities.utilisateurs import Utilisateur
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementInconnu,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.identite.value_objects.organisme_action import OrganismeAction
from domain.recruteur.value_objects.roles import (
    AgentOrganismeRole,
    AgentRecrutementRole,
)
from infrastructure.django_apps.users.models import UserModel
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeAgentDjangoFactory,
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementAgentDjangoFactory,
    RecrutementDjangoFactory,
)

pytestmark = pytest.mark.django_db


STAFF_SEULEMENT_SANS_ORGANISME_ACTIONS = [
    OrganismeAction.CREER_ORGANISME,
    OrganismeAction.LISTER_ORGANISMES,
]

STAFF_SEULEMENT_AVEC_ORGANISME_ACTIONS = [
    OrganismeAction.MODIFIER_ORGANISME,
]

SUPERVISEUR_ET_STAFF_ACTIONS = [
    OrganismeAction.GET_ORGANISME,
    OrganismeAction.INITIALIZE_ORGANISME_STEPS,
    OrganismeAction.UPDATE_ORGANISME_STEPS,
    OrganismeAction.LIST_ORGANISME_AGENTS,
    OrganismeAction.ATTACH_ORGANISME_AGENT,
    OrganismeAction.UPDATE_ORGANISME_AGENT,
    OrganismeAction.REVOKE_ORGANISME_AGENT,
    OrganismeAction.SET_RECRUTEMENTS_RESPONSABLE,
]

SUPERVISEUR_OU_AGENT_RESPONSABLE_D_UN_RECRUTEMENT_ACTIONS = [
    OrganismeAction.SEARCH_AGENT,
    OrganismeAction.CREATE_AGENT,
]

SUPERVISEUR_OU_AGENT_SANS_RECRUTEMENT_ACTIONS = [
    OrganismeAction.LIST_RECRUTEMENTS,
    OrganismeAction.GET_MOTIFS_REFUS,
]

SUPERVISEUR_OU_AGENT_AVEC_RECRUTEMENT_ACTIONS = [
    OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
    OrganismeAction.GET_CANDIDATURE_DETAIL,
    OrganismeAction.READ_DOCUMENT,
    OrganismeAction.LIST_DOCUMENTS,
    OrganismeAction.LIST_NOTES,
    OrganismeAction.CREATE_NOTE,
    OrganismeAction.UPDATE_NOTE,
    OrganismeAction.DELETE_NOTE,
    OrganismeAction.LIST_CONVERSATIONS,
    OrganismeAction.READ_CONVERSATION,
    OrganismeAction.CREATE_CONVERSATION,
    OrganismeAction.REPLY_CONVERSATION,
]
SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_ACTIONS = [
    OrganismeAction.GET_RECRUTEMENT_ETAPES,
    OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
    OrganismeAction.INIT_RECRUTEMENT_ETAPES,
    OrganismeAction.LIST_RECRUTEMENT_AGENTS,
    OrganismeAction.ADD_RECRUTEMENT_AGENT,
    OrganismeAction.UPDATE_RECRUTEMENT_AGENT,
    OrganismeAction.REVOKE_RECRUTEMENT_AGENT,
]

SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_OU_RECRUTEUR_ACTIONS = [
    OrganismeAction.CHANGER_ETAPE_CANDIDATURES,
]

SUPERVISEUR_ACTIONS = (
    SUPERVISEUR_ET_STAFF_ACTIONS
    + SUPERVISEUR_OU_AGENT_RESPONSABLE_D_UN_RECRUTEMENT_ACTIONS
    + SUPERVISEUR_OU_AGENT_SANS_RECRUTEMENT_ACTIONS
    + SUPERVISEUR_OU_AGENT_AVEC_RECRUTEMENT_ACTIONS
    + SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_ACTIONS
    + SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_OU_RECRUTEUR_ACTIONS
)

SUPERVISEUR_ACTIONS_SANS_RECRUTEMENT = (
    SUPERVISEUR_ET_STAFF_ACTIONS
    + SUPERVISEUR_OU_AGENT_RESPONSABLE_D_UN_RECRUTEMENT_ACTIONS
    + SUPERVISEUR_OU_AGENT_SANS_RECRUTEMENT_ACTIONS
)

RECRUTEMENT_ACTIONS = (
    SUPERVISEUR_OU_AGENT_AVEC_RECRUTEMENT_ACTIONS
    + SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_ACTIONS
    + SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_OU_RECRUTEUR_ACTIONS
)


ConstruireUtilisateur = Callable[..., Utilisateur | UserModel]


@pytest.fixture(params=["utilisateur", "user_model"])
def utilisateur_de(request: pytest.FixtureRequest) -> ConstruireUtilisateur:
    def construire(
        entity_id: UUID, *, is_staff: bool = False
    ) -> Utilisateur | UserModel:
        if request.param == "user_model":
            return UserModel(username=entity_id, is_staff=is_staff)
        return UtilisateurFactory.create_entity(entity_id=entity_id, is_staff=is_staff)

    return construire


def _attach_recrutement_role(
    organisme, agent, role: AgentRecrutementRole, *, revoked: bool = False
):
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    RecrutementAgentDjangoFactory(
        recrutement=recrutement,
        agent=agent,
        role=role.value,
        date_revocation=timezone.now() if revoked else None,
    )
    return recrutement


class TestActionsIntegrity:
    def test_every_agent_action_is_classified(self) -> None:
        actions_membre = frozenset(
            action
            for action, roles in _ROLES_REQUIS.items()
            if AgentOrganismeRole.AGENT in roles
        )

        assert actions_membre <= (
            _ROLES_RECRUTEMENT_REQUIS.keys()
            | _SANS_ROLE_RECRUTEMENT_REQUIS
            | _RESPONSABLE_D_UN_RECRUTEMENT_REQUIS
        )

    def test_all_actions_are_covered_only_once(self) -> None:
        cases = [
            STAFF_SEULEMENT_SANS_ORGANISME_ACTIONS,
            STAFF_SEULEMENT_AVEC_ORGANISME_ACTIONS,
            SUPERVISEUR_ET_STAFF_ACTIONS,
            SUPERVISEUR_OU_AGENT_RESPONSABLE_D_UN_RECRUTEMENT_ACTIONS,
            SUPERVISEUR_OU_AGENT_SANS_RECRUTEMENT_ACTIONS,
            SUPERVISEUR_OU_AGENT_AVEC_RECRUTEMENT_ACTIONS,
            SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_ACTIONS,
            SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_OU_RECRUTEUR_ACTIONS,
        ]
        actions = [action for liste in cases for action in liste]

        assert len(actions) == len(OrganismeAction)
        assert set(actions) == set(OrganismeAction)


@pytest.mark.parametrize("action", SUPERVISEUR_ET_STAFF_ACTIONS)
class TestSuperviseurEtStaffActions:
    def test_superviseur_actions_allowed_superviseur_role(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
        )

        assert result == AgentOrganismeRole.SUPERVISEUR

    @pytest.mark.parametrize(
        "role",
        [AgentOrganismeRole.AGENT, None],
        ids=["membre_role", "no_organisme_role"],
    )
    def test_supreviseur_actions_reject_non_superviseur_role(
        self,
        utilisateur_de: ConstruireUtilisateur,
        action: OrganismeAction,
        role: AgentOrganismeRole | None,
    ) -> None:
        if role is None:
            organisme = OrganismeDjangoFactory()
            demandeur_id = uuid4()
        else:
            agent, organisme = create_organisme_with_agent(role=role)
            demandeur_id = agent.utilisateur_id

        with pytest.raises(AccesOrganismeRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,  # type: ignore[arg-type]
                utilisateur=utilisateur_de(demandeur_id),
            )


@pytest.mark.parametrize("action", SUPERVISEUR_OU_AGENT_SANS_RECRUTEMENT_ACTIONS)
class TestSuperviseurOuAgentSansRecrutementActions:
    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.SUPERVISEUR, AgentOrganismeRole.AGENT]
    )
    def test_allow_superviseur_and_agent(
        self,
        utilisateur_de: ConstruireUtilisateur,
        action: OrganismeAction,
        role: AgentOrganismeRole,
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=role)

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
        )

        assert result == role

    def test_reject_no_role(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        organisme = OrganismeDjangoFactory()

        with pytest.raises(AccesOrganismeRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,  # type: ignore[arg-type]
                utilisateur=utilisateur_de(uuid4()),
            )


REVOKED_LIAISON_CASES = [
    *[
        (action, AgentOrganismeRole.SUPERVISEUR)
        for action in SUPERVISEUR_ET_STAFF_ACTIONS
    ],
    *[
        (action, AgentOrganismeRole.AGENT)
        for action in SUPERVISEUR_OU_AGENT_SANS_RECRUTEMENT_ACTIONS
    ],
]


@pytest.mark.parametrize(("action", "role"), REVOKED_LIAISON_CASES)
def test_revoked_liaison_is_denied(
    utilisateur_de: ConstruireUtilisateur,
    action: OrganismeAction,
    role: AgentOrganismeRole,
) -> None:
    organisme = OrganismeDjangoFactory()
    agent = OrganismeAgentDjangoFactory(
        organisme=organisme,
        role=role.value,
        date_revocation=timezone.now(),
    ).agent

    with pytest.raises(AccesOrganismeRefuse):
        OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,  # type: ignore[arg-type]
            utilisateur=utilisateur_de(agent.utilisateur_id),  # type: ignore[attr-defined]
        )


def test_revocation_is_scoped_to_organisme(
    utilisateur_de: ConstruireUtilisateur,
) -> None:
    organisme_a = OrganismeDjangoFactory()
    agent = OrganismeAgentDjangoFactory(
        organisme=organisme_a,
        role=AgentOrganismeRole.AGENT.value,
        date_revocation=timezone.now(),
    ).agent
    recrutement_a = _attach_recrutement_role(
        organisme_a, agent, AgentRecrutementRole.CONTRIBUTEUR
    )
    organisme_b = OrganismeDjangoFactory()
    OrganismeAgentDjangoFactory(
        organisme=organisme_b, agent=agent, role=AgentOrganismeRole.AGENT.value
    )
    recrutement_b = _attach_recrutement_role(
        organisme_b, agent, AgentRecrutementRole.CONTRIBUTEUR
    )

    result = OrganismePermissionService().can_execute(
        action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
        organisme_id=organisme_b.id,  # type: ignore[arg-type]
        utilisateur=utilisateur_de(agent.utilisateur_id),  # type: ignore[attr-defined]
        recrutement_id=recrutement_b.pk,
    )

    assert result == AgentOrganismeRole.AGENT
    with pytest.raises(AccesOrganismeRefuse):
        OrganismePermissionService().can_execute(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=organisme_a.id,  # type: ignore[arg-type]
            utilisateur=utilisateur_de(agent.utilisateur_id),  # type: ignore[attr-defined]
            recrutement_id=recrutement_a.pk,
        )


@pytest.mark.parametrize("action", SUPERVISEUR_OU_AGENT_AVEC_RECRUTEMENT_ACTIONS)
class TestSuperviseurOuAgentAvecRecrutementActions:
    @pytest.mark.parametrize("recrutement_role", list(AgentRecrutementRole))
    def test_agent_with_recrutement_role_is_allowed(
        self,
        utilisateur_de: ConstruireUtilisateur,
        action: OrganismeAction,
        recrutement_role: AgentRecrutementRole,
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        recrutement = _attach_recrutement_role(organisme, agent, recrutement_role)

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
            recrutement_id=recrutement.pk,
        )

        assert result == AgentOrganismeRole.AGENT

    def test_superviseur_bypasses_recrutement_check(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
            recrutement_id=uuid4(),
        )

        assert result == AgentOrganismeRole.SUPERVISEUR

    def test_agent_without_recrutement_role_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
                recrutement_id=uuid4(),
            )

    def test_unprovided_recrutement_id_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)

        with pytest.raises(AccesRecrutementInconnu):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
            )

    def test_agent_with_revoked_recrutement_role_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        recrutement = _attach_recrutement_role(
            organisme, agent, AgentRecrutementRole.RESPONSABLE, revoked=True
        )

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
                recrutement_id=recrutement.pk,
            )


@pytest.mark.parametrize("action", SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_ACTIONS)
class TestSuperviseurOuAgentAvecResponsableActions:
    def test_superviseur_bypasses_recrutement_check(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
            recrutement_id=uuid4(),
        )

        assert result == AgentOrganismeRole.SUPERVISEUR

    def test_agent_with_responsable_role_is_allowed(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        recrutement = _attach_recrutement_role(
            organisme, agent, AgentRecrutementRole.RESPONSABLE
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
            recrutement_id=recrutement.pk,
        )

        assert result == AgentOrganismeRole.AGENT

    @pytest.mark.parametrize(
        "recrutement_role",
        [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR, None],
    )
    def test_agent_without_responsable_role_is_denied(
        self,
        utilisateur_de: ConstruireUtilisateur,
        action: OrganismeAction,
        recrutement_role: AgentRecrutementRole | None,
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        if recrutement_role is None:
            recrutement_id = uuid4()
        else:
            recrutement_id = _attach_recrutement_role(
                organisme, agent, recrutement_role
            ).pk

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
                recrutement_id=recrutement_id,
            )

    def test_unprovided_recrutement_id_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)

        with pytest.raises(AccesRecrutementInconnu):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
            )

    def test_agent_with_revoked_responsable_role_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        recrutement = _attach_recrutement_role(
            organisme, agent, AgentRecrutementRole.RESPONSABLE, revoked=True
        )

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
                recrutement_id=recrutement.pk,
            )


@pytest.mark.parametrize(
    "action", SUPERVISEUR_OU_AGENT_RESPONSABLE_D_UN_RECRUTEMENT_ACTIONS
)
class TestSuperviseurOuAgentResponsableDUnRecrutementActions:
    def test_superviseur_is_allowed(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
        )

        assert result == AgentOrganismeRole.SUPERVISEUR

    def test_agent_responsable_of_a_recrutement_is_allowed(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        _attach_recrutement_role(organisme, agent, AgentRecrutementRole.RESPONSABLE)

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
        )

        assert result == AgentOrganismeRole.AGENT

    @pytest.mark.parametrize(
        "recrutement_role",
        [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR, None],
    )
    def test_agent_not_responsable_is_denied(
        self,
        utilisateur_de: ConstruireUtilisateur,
        action: OrganismeAction,
        recrutement_role: AgentRecrutementRole | None,
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        if recrutement_role is not None:
            _attach_recrutement_role(organisme, agent, recrutement_role)

        with pytest.raises(AccesOrganismeRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
            )

    def test_agent_responsable_in_another_organisme_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        autre_organisme = OrganismeDjangoFactory()
        _attach_recrutement_role(
            autre_organisme, agent, AgentRecrutementRole.RESPONSABLE
        )

        with pytest.raises(AccesOrganismeRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
            )

    def test_agent_with_revoked_responsable_role_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        _attach_recrutement_role(
            organisme, agent, AgentRecrutementRole.RESPONSABLE, revoked=True
        )

        with pytest.raises(AccesOrganismeRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
            )


@pytest.mark.parametrize(
    "action", SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_OU_RECRUTEUR_ACTIONS
)
class TestSuperviseurOuAgentAvecResponsableOuRecruteurActions:
    def test_superviseur_bypasses_recrutement_check(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
            recrutement_id=uuid4(),
        )

        assert result == AgentOrganismeRole.SUPERVISEUR

    @pytest.mark.parametrize(
        "recrutement_role",
        [AgentRecrutementRole.RESPONSABLE, AgentRecrutementRole.RECRUTEUR],
    )
    def test_agent_with_responsable_or_recruteur_role_is_allowed(
        self,
        utilisateur_de: ConstruireUtilisateur,
        action: OrganismeAction,
        recrutement_role: AgentRecrutementRole,
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        recrutement = _attach_recrutement_role(organisme, agent, recrutement_role)

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
            recrutement_id=recrutement.pk,
        )

        assert result == AgentOrganismeRole.AGENT

    @pytest.mark.parametrize(
        "recrutement_role", [AgentRecrutementRole.CONTRIBUTEUR, None]
    )
    def test_agent_without_responsable_or_recruteur_role_is_denied(
        self,
        utilisateur_de: ConstruireUtilisateur,
        action: OrganismeAction,
        recrutement_role: AgentRecrutementRole | None,
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        if recrutement_role is None:
            recrutement_id = uuid4()
        else:
            recrutement_id = _attach_recrutement_role(
                organisme, agent, recrutement_role
            ).pk

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
                recrutement_id=recrutement_id,
            )

    def test_unprovided_recrutement_id_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)

        with pytest.raises(AccesRecrutementInconnu):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
            )

    def test_agent_with_revoked_recruteur_role_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
        recrutement = _attach_recrutement_role(
            organisme, agent, AgentRecrutementRole.RECRUTEUR, revoked=True
        )

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id),
                recrutement_id=recrutement.pk,
            )


@pytest.mark.parametrize("action", RECRUTEMENT_ACTIONS)
def test_role_on_a_recrutement_does_not_grant_access_to_another_one(
    utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
) -> None:
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    _attach_recrutement_role(organisme, agent, AgentRecrutementRole.RESPONSABLE)
    autre_recrutement = RecrutementDjangoFactory(organisme=organisme)

    with pytest.raises(AccesRecrutementRefuse):
        OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=utilisateur_de(agent.utilisateur_id),
            recrutement_id=autre_recrutement.pk,  # type: ignore[attr-defined]
        )


class TestOrganismeExistenceGuard:
    def test_raises_when_organisme_not_found(
        self, utilisateur_de: ConstruireUtilisateur
    ) -> None:
        organisme_id = uuid4()

        with pytest.raises(OrganismeNexistePas):
            OrganismePermissionService().can_execute(
                action=OrganismeAction.GET_ORGANISME,
                organisme_id=organisme_id,
                utilisateur=utilisateur_de(uuid4()),
            )

    def test_organisme_guard_runs_before_staff_bypass_and_role_check(
        self, utilisateur_de: ConstruireUtilisateur
    ) -> None:
        organisme_id = uuid4()

        with pytest.raises(OrganismeNexistePas):
            OrganismePermissionService().can_execute(
                action=OrganismeAction.GET_ORGANISME,
                organisme_id=organisme_id,
                utilisateur=utilisateur_de(uuid4(), is_staff=True),
            )

    @pytest.mark.parametrize("is_staff", [False, True], ids=["superviseur", "staff"])
    def test_raises_when_organisme_supprime(
        self, utilisateur_de: ConstruireUtilisateur, is_staff: bool
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.SUPERVISEUR, supprime_le=timezone.now()
        )

        with pytest.raises(OrganismeNexistePas):
            OrganismePermissionService().can_execute(
                action=OrganismeAction.GET_ORGANISME,
                organisme_id=organisme.id,
                utilisateur=utilisateur_de(agent.utilisateur_id, is_staff=is_staff),
            )


@pytest.mark.parametrize("action", STAFF_SEULEMENT_SANS_ORGANISME_ACTIONS)
class TestStaffSeulementSansOrganismeActions:
    def test_staff_can_execute(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        result = OrganismePermissionService().can_execute(
            action=action,
            utilisateur=utilisateur_de(uuid4(), is_staff=True),
        )

        assert result is None


@pytest.mark.parametrize("action", STAFF_SEULEMENT_AVEC_ORGANISME_ACTIONS)
class TestStaffSeulementAvecOrganismeActions:
    def test_staff_can_execute(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        organisme = OrganismeDjangoFactory()

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,  # type: ignore[arg-type]
            utilisateur=utilisateur_de(uuid4(), is_staff=True),
        )

        assert result is None

    def test_non_staff_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        organisme = OrganismeDjangoFactory()

        with pytest.raises(OperationOrganismeRefusee):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,  # type: ignore[arg-type]
                utilisateur=utilisateur_de(uuid4()),
            )

    def test_organisme_check_runs_before_staff_check(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        organisme_id = uuid4()

        with pytest.raises(OrganismeNexistePas):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme_id,
                utilisateur=utilisateur_de(uuid4(), is_staff=True),
            )


@pytest.mark.parametrize("action", SUPERVISEUR_ACTIONS)
class TestStaffActsAsSuperviseur:
    @pytest.mark.parametrize(
        "organisme_role",
        [None, AgentOrganismeRole.AGENT],
        ids=["no_organisme_role", "membre_role"],
    )
    def test_staff_gets_superviseur_role(
        self,
        utilisateur_de: ConstruireUtilisateur,
        action: OrganismeAction,
        organisme_role: AgentOrganismeRole | None,
    ) -> None:
        if organisme_role is None:
            organisme = OrganismeDjangoFactory()
            demandeur_id = uuid4()
        else:
            agent, organisme = create_organisme_with_agent(role=organisme_role)
            demandeur_id = agent.utilisateur_id
        recrutement_id = (
            RecrutementDjangoFactory(organisme=organisme).pk  # type: ignore[attr-defined]
            if action in RECRUTEMENT_ACTIONS
            else None
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,  # type: ignore[arg-type]
            utilisateur=utilisateur_de(demandeur_id, is_staff=True),
            recrutement_id=recrutement_id,
        )

        assert result == AgentOrganismeRole.SUPERVISEUR

    def test_staff_without_organisme_id_is_denied(
        self, utilisateur_de: ConstruireUtilisateur, action: OrganismeAction
    ) -> None:
        with pytest.raises(AccesOrganismeRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                utilisateur=utilisateur_de(uuid4(), is_staff=True),
            )


def test_superviseur_of_another_organisme_is_denied(
    utilisateur_de: ConstruireUtilisateur,
) -> None:
    agent, _ = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    organisme = OrganismeDjangoFactory()

    with pytest.raises(AccesOrganismeRefuse):
        OrganismePermissionService().can_execute(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=organisme.id,  # type: ignore[arg-type]
            utilisateur=utilisateur_de(agent.utilisateur_id),
        )


class TestAuthorizedActions:
    @pytest.mark.parametrize(
        ("is_staff", "expected"),
        [
            (False, []),
            (
                True,
                [
                    OrganismeAction.CREER_ORGANISME,
                    OrganismeAction.LISTER_ORGANISMES,
                    OrganismeAction.MODIFIER_ORGANISME,
                ],
            ),
        ],
        ids=["non_staff", "staff"],
    )
    def test_user_authorized_actions(self, is_staff, expected):
        assert (
            OrganismePermissionService().actions_autorisees_utilisateur(
                UserModel(is_staff=is_staff)
            )
            == expected
        )

    def test_agent_gets_actions_without_target_recrutement(self):
        assert OrganismePermissionService().actions_autorisees_organisme(
            AgentOrganismeRole.AGENT,
            utilisateur=UserModel(is_staff=False),
            organisme_id=uuid4(),
            organisme_ids_responsable={uuid4()},
        ) == [
            OrganismeAction.LIST_RECRUTEMENTS,
            OrganismeAction.GET_MOTIFS_REFUS,
        ]

    def test_superviseur_gets_actions_without_target_recrutement(self):
        assert OrganismePermissionService().actions_autorisees_organisme(
            AgentOrganismeRole.SUPERVISEUR,
            utilisateur=UserModel(is_staff=False),
            organisme_id=uuid4(),
            organisme_ids_responsable=set(),
        ) == sorted(
            SUPERVISEUR_ACTIONS_SANS_RECRUTEMENT, key=list(OrganismeAction).index
        )

    def test_responsable_agent_gets_search_and_create_agent(self):
        organisme_id = uuid4()

        assert OrganismePermissionService().actions_autorisees_organisme(
            AgentOrganismeRole.AGENT,
            utilisateur=UserModel(is_staff=False),
            organisme_id=organisme_id,
            organisme_ids_responsable={organisme_id},
        ) == [
            OrganismeAction.LIST_RECRUTEMENTS,
            OrganismeAction.SEARCH_AGENT,
            OrganismeAction.CREATE_AGENT,
            OrganismeAction.GET_MOTIFS_REFUS,
        ]

    @pytest.mark.parametrize("is_responsable", [False, True])
    def test_staff_acts_as_superviseur(self, is_responsable):
        organisme_id = uuid4()

        assert OrganismePermissionService().actions_autorisees_organisme(
            AgentOrganismeRole.AGENT,
            utilisateur=UserModel(is_staff=True),
            organisme_id=organisme_id,
            organisme_ids_responsable={organisme_id} if is_responsable else set(),
        ) == sorted(
            SUPERVISEUR_ACTIONS_SANS_RECRUTEMENT, key=list(OrganismeAction).index
        )

    @pytest.mark.parametrize(
        ("role", "is_responsable"),
        [
            (AgentOrganismeRole.SUPERVISEUR, False),
            (AgentOrganismeRole.AGENT, False),
            (AgentOrganismeRole.AGENT, True),
        ],
    )
    def test_every_exposed_action_is_accepted_by_can_execute(
        self, role, is_responsable
    ):
        agent, organisme = create_organisme_with_agent(role=role)
        if is_responsable:
            _attach_recrutement_role(organisme, agent, AgentRecrutementRole.RESPONSABLE)

        for action in OrganismePermissionService().actions_autorisees_organisme(
            role,
            utilisateur=agent.utilisateur,
            organisme_id=organisme.id,
            organisme_ids_responsable={organisme.id} if is_responsable else set(),
        ):
            OrganismePermissionService().can_execute(
                action=action, utilisateur=agent.utilisateur, organisme_id=organisme.id
            )
