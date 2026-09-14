from uuid import UUID, uuid4

import pytest
from django.utils import timezone

from application.identite.context_services.organisme_permission_service import (
    _ROLES_RECRUTEMENT_REQUIS,
    _ROLES_REQUIS,
    _SANS_ROLE_RECRUTEMENT_REQUIS,
    OrganismePermissionService,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
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

# TODO: add test for CHANGER_ETAPE_CANDIDATURES

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
    OrganismeAction.SEARCH_AGENT,
    OrganismeAction.ATTACH_ORGANISME_AGENT,
    OrganismeAction.UPDATE_ORGANISME_AGENT,
    OrganismeAction.REVOKE_ORGANISME_AGENT,
    OrganismeAction.CREATE_AGENT,
    OrganismeAction.LIST_RECRUTEMENT_AGENTS,
    OrganismeAction.ADD_RECRUTEMENT_AGENT,
    OrganismeAction.UPDATE_RECRUTEMENT_AGENT,
    OrganismeAction.REVOKE_RECRUTEMENT_AGENT,
]

SUPERVISEUR_OU_AGENT_SANS_RECRUTEMENT_ACTIONS = [
    OrganismeAction.LISTER_MES_RECRUTEMENTS,
]

SUPERVISEUR_OU_AGENT_AVEC_RECRUTEMENT_ACTIONS = [
    OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
]
SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_ACTIONS = [
    OrganismeAction.GET_RECRUTEMENT_ETAPES,
    OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
    OrganismeAction.INIT_RECRUTEMENT_ETAPES,
]

SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_OU_RECRUTEUR_ACTIONS = [
    OrganismeAction.CHANGER_ETAPE_CANDIDATURES,
]


def _utilisateur(entity_id: UUID, *, is_staff: bool = False):
    return UtilisateurFactory.create_entity(entity_id=entity_id, is_staff=is_staff)


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
    def test_toute_action_membre_est_classee(self) -> None:
        actions_membre = frozenset(
            action
            for action, roles in _ROLES_REQUIS.items()
            if AgentOrganismeRole.MEMBRE in roles
        )

        assert actions_membre <= (
            _ROLES_RECRUTEMENT_REQUIS.keys() | _SANS_ROLE_RECRUTEMENT_REQUIS
        )

    def test_toutes_les_actions_sont_couvertes_une_seule_fois(self) -> None:
        cas = [
            STAFF_SEULEMENT_SANS_ORGANISME_ACTIONS,
            STAFF_SEULEMENT_AVEC_ORGANISME_ACTIONS,
            SUPERVISEUR_ET_STAFF_ACTIONS,
            SUPERVISEUR_OU_AGENT_SANS_RECRUTEMENT_ACTIONS,
            SUPERVISEUR_OU_AGENT_AVEC_RECRUTEMENT_ACTIONS,
            SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_ACTIONS,
            SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_OU_RECRUTEUR_ACTIONS,
        ]
        actions_classees = [action for liste in cas for action in liste]

        assert len(actions_classees) == len(OrganismeAction)
        assert set(actions_classees) == set(OrganismeAction)


@pytest.mark.parametrize("action", SUPERVISEUR_ET_STAFF_ACTIONS)
class TestSuperviseurEtStaffActions:
    def test_responsable_actions_allow_responsable(
        self, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

        assert result == AgentOrganismeRole.RESPONSABLE

    def test_staff_bypasses_role_check(self, action: OrganismeAction) -> None:
        organisme = OrganismeDjangoFactory()

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,  # type: ignore[arg-type]
            utilisateur=_utilisateur(uuid4(), is_staff=True),
        )

        assert result is None

    @pytest.mark.parametrize(
        "role",
        [AgentOrganismeRole.MEMBRE, None],
        ids=["membre_role", "no_organisme_role"],
    )
    def test_responsable_actions_reject_non_responsable(
        self, action: OrganismeAction, role: AgentOrganismeRole | None
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
                utilisateur=_utilisateur(demandeur_id),
            )

    def test_revoked_agent_is_still_allowed(self, action: OrganismeAction) -> None:
        # Documents current behavior: unlike the recrutement-agent lookup, the
        # organisme-agent role lookup does not filter out revoked agents.
        organisme = OrganismeDjangoFactory()
        agent = OrganismeAgentDjangoFactory(
            organisme=organisme,
            role=AgentOrganismeRole.RESPONSABLE.value,
            date_revocation=timezone.now(),
        ).agent

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,  # type: ignore[arg-type]
            utilisateur=_utilisateur(agent.utilisateur_id),  # type: ignore[attr-defined]
        )

        assert result == AgentOrganismeRole.RESPONSABLE


@pytest.mark.parametrize("action", SUPERVISEUR_OU_AGENT_SANS_RECRUTEMENT_ACTIONS)
class TestSuperviseurOuAgentSansRecrutementActions:
    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE]
    )
    def test_allow_responsable_and_membre(
        self, action: OrganismeAction, role: AgentOrganismeRole
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=role)

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

        assert result == role

    @pytest.mark.parametrize("est_staff", [False, True])
    def test_reject_no_role_nor_staff(
        self, action: OrganismeAction, est_staff: bool
    ) -> None:
        organisme = OrganismeDjangoFactory()

        with pytest.raises(AccesOrganismeRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,  # type: ignore[arg-type]
                utilisateur=_utilisateur(uuid4(), is_staff=est_staff),
            )


@pytest.mark.parametrize("action", SUPERVISEUR_OU_AGENT_AVEC_RECRUTEMENT_ACTIONS)
class TestSuperviseurOuAgentAvecRecrutementActions:
    @pytest.mark.parametrize("recrutement_role", list(AgentRecrutementRole))
    def test_membre_with_recrutement_role_is_allowed(
        self, action: OrganismeAction, recrutement_role: AgentRecrutementRole
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = _attach_recrutement_role(organisme, agent, recrutement_role)

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
            recrutement_id=recrutement.pk,
        )

        assert result == AgentOrganismeRole.MEMBRE

    def test_responsable_bypasses_recrutement_check(
        self, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
            recrutement_id=uuid4(),
        )

        assert result == AgentOrganismeRole.RESPONSABLE

    def test_membre_without_recrutement_role_is_denied(
        self, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(agent.utilisateur_id),
                recrutement_id=uuid4(),
            )

    def test_unprovided_recrutement_id_is_denied(self, action: OrganismeAction) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)

        with pytest.raises(AccesRecrutementInconnu):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

    def test_staff_without_role_is_denied(self, action: OrganismeAction) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(agent.utilisateur_id, is_staff=True),
                recrutement_id=uuid4(),
            )

    def test_membre_with_revoked_recrutement_role_is_denied(
        self, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = _attach_recrutement_role(
            organisme, agent, AgentRecrutementRole.RESPONSABLE, revoked=True
        )

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(agent.utilisateur_id),
                recrutement_id=recrutement.pk,
            )


@pytest.mark.parametrize("action", SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_ACTIONS)
class TestSuperviseurOuAgentAvecResponsableActions:
    def test_organisme_responsable_bypasses_recrutement_check(
        self, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
            recrutement_id=uuid4(),
        )

        assert result == AgentOrganismeRole.RESPONSABLE

    def test_membre_with_recrutement_responsable_is_allowed(
        self, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = _attach_recrutement_role(
            organisme, agent, AgentRecrutementRole.RESPONSABLE
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
            recrutement_id=recrutement.pk,
        )

        assert result == AgentOrganismeRole.MEMBRE

    @pytest.mark.parametrize(
        "recrutement_role",
        [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR, None],
    )
    def test_membre_without_recrutement_responsable_is_denied(
        self, action: OrganismeAction, recrutement_role: AgentRecrutementRole | None
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
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
                utilisateur=_utilisateur(agent.utilisateur_id),
                recrutement_id=recrutement_id,
            )

    def test_unprovided_recrutement_id_is_denied(self, action: OrganismeAction) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)

        with pytest.raises(AccesRecrutementInconnu):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

    def test_staff_without_organisme_role_is_denied(
        self, action: OrganismeAction
    ) -> None:
        organisme = OrganismeDjangoFactory()

        with pytest.raises(AccesOrganismeRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,  # type: ignore[arg-type]
                utilisateur=_utilisateur(uuid4(), is_staff=True),
                recrutement_id=uuid4(),
            )

    def test_membre_with_revoked_recrutement_responsable_is_denied(
        self, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = _attach_recrutement_role(
            organisme, agent, AgentRecrutementRole.RESPONSABLE, revoked=True
        )

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(agent.utilisateur_id),
                recrutement_id=recrutement.pk,
            )


@pytest.mark.parametrize(
    "action", SUPERVISEUR_OU_AGENT_AVEC_RESPONSABLE_OU_RECRUTEUR_ACTIONS
)
class TestSuperviseurOuAgentAvecResponsableOuRecruteurActions:
    def test_organisme_responsable_bypasses_recrutement_check(
        self, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE
        )

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
            recrutement_id=uuid4(),
        )

        assert result == AgentOrganismeRole.RESPONSABLE

    @pytest.mark.parametrize(
        "recrutement_role",
        [AgentRecrutementRole.RESPONSABLE, AgentRecrutementRole.RECRUTEUR],
    )
    def test_membre_with_recrutement_responsable_or_recruteur_is_allowed(
        self, action: OrganismeAction, recrutement_role: AgentRecrutementRole
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = _attach_recrutement_role(organisme, agent, recrutement_role)

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
            recrutement_id=recrutement.pk,
        )

        assert result == AgentOrganismeRole.MEMBRE

    @pytest.mark.parametrize(
        "recrutement_role", [AgentRecrutementRole.CONTRIBUTEUR, None]
    )
    def test_membre_without_recrutement_responsable_or_recruteur_is_denied(
        self, action: OrganismeAction, recrutement_role: AgentRecrutementRole | None
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
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
                utilisateur=_utilisateur(agent.utilisateur_id),
                recrutement_id=recrutement_id,
            )

    def test_unprovided_recrutement_id_is_denied(self, action: OrganismeAction) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)

        with pytest.raises(AccesRecrutementInconnu):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(agent.utilisateur_id),
            )

    def test_staff_without_organisme_role_is_denied(
        self, action: OrganismeAction
    ) -> None:
        organisme = OrganismeDjangoFactory()

        with pytest.raises(AccesOrganismeRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,  # type: ignore[arg-type]
                utilisateur=_utilisateur(uuid4(), is_staff=True),
                recrutement_id=uuid4(),
            )

    def test_membre_with_revoked_recrutement_recruteur_is_denied(
        self, action: OrganismeAction
    ) -> None:
        agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = _attach_recrutement_role(
            organisme, agent, AgentRecrutementRole.RECRUTEUR, revoked=True
        )

        with pytest.raises(AccesRecrutementRefuse):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(agent.utilisateur_id),
                recrutement_id=recrutement.pk,
            )


class TestOrganismeExistenceGuard:
    def test_raises_when_organisme_not_found(self) -> None:
        organisme_id = uuid4()

        with pytest.raises(OrganismeNexistePas):
            OrganismePermissionService().can_execute(
                action=OrganismeAction.GET_ORGANISME,
                organisme_id=organisme_id,
                utilisateur=_utilisateur(uuid4()),
            )

    def test_organisme_guard_runs_before_staff_bypass_and_role_check(self) -> None:
        organisme_id = uuid4()

        with pytest.raises(OrganismeNexistePas):
            OrganismePermissionService().can_execute(
                action=OrganismeAction.GET_ORGANISME,
                organisme_id=organisme_id,
                utilisateur=_utilisateur(uuid4(), is_staff=True),
            )


@pytest.mark.parametrize("action", STAFF_SEULEMENT_SANS_ORGANISME_ACTIONS)
class TestStaffSeulementSansOrganismeActions:
    def test_staff_can_execute(self, action: OrganismeAction) -> None:
        result = OrganismePermissionService().can_execute(
            action=action,
            utilisateur=_utilisateur(uuid4(), is_staff=True),
        )

        assert result is None


@pytest.mark.parametrize("action", STAFF_SEULEMENT_AVEC_ORGANISME_ACTIONS)
class TestStaffSeulementAvecOrganismeActions:
    def test_staff_can_execute(self, action: OrganismeAction) -> None:
        organisme = OrganismeDjangoFactory()

        result = OrganismePermissionService().can_execute(
            action=action,
            organisme_id=organisme.id,  # type: ignore[arg-type]
            utilisateur=_utilisateur(uuid4(), is_staff=True),
        )

        assert result is None

    def test_non_staff_est_refuse_apres_verification_existence(
        self, action: OrganismeAction
    ) -> None:
        organisme = OrganismeDjangoFactory()

        with pytest.raises(OperationOrganismeRefusee):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme.id,  # type: ignore[arg-type]
                utilisateur=_utilisateur(uuid4()),
            )

    def test_organisme_inexistant_est_priorise_sur_le_statut_staff(
        self, action: OrganismeAction
    ) -> None:
        organisme_id = uuid4()

        with pytest.raises(OrganismeNexistePas):
            OrganismePermissionService().can_execute(
                action=action,
                organisme_id=organisme_id,
                utilisateur=_utilisateur(uuid4(), is_staff=True),
            )
