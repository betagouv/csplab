from uuid import uuid4

import pytest
from django.utils import timezone

from application.identite.context_services.organisme_permission_service import (
    _ROLES_RECRUTEMENT_REQUIS,
    _ROLES_REQUIS,
    _SANS_ROLE_RECRUTEMENT_REQUIS,
    can_execute,
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

# TODO: add test for CHANGER_ETAPE_CANDIDATURES

RESPONSABLE_ACTIONS = [
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

RECRUTEMENT_ETAPES_ACTIONS = [
    OrganismeAction.GET_RECRUTEMENT_ETAPES,
    OrganismeAction.UPDATE_RECRUTEMENT_ETAPES,
    OrganismeAction.INIT_RECRUTEMENT_ETAPES,
]

ACTIONS_SANS_ORGANISME = [
    OrganismeAction.CREER_ORGANISME,
    OrganismeAction.LISTER_ORGANISMES,
]


def _utilisateur(entity_id, *, is_staff=False):
    return UtilisateurFactory.create_entity(entity_id=entity_id, is_staff=is_staff)


@pytest.mark.parametrize("action", RESPONSABLE_ACTIONS)
class TestResponsableActions:
    def test_responsable_actions_allow_responsable(self, db, action):
        responsable, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE
        )

        result = can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(responsable.utilisateur_id),
        )

        assert result == AgentOrganismeRole.RESPONSABLE

    def test_staff_bypasses_role_check(self, db, action):
        organisme = OrganismeDjangoFactory()

        result = can_execute(
            action=action,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(uuid4(), is_staff=True),
        )

        assert result is None

    @pytest.mark.parametrize("role", [AgentOrganismeRole.MEMBRE, None])
    def test_responsable_actions_reject_non_responsable(self, db, action, role):
        if role is None:
            organisme = OrganismeDjangoFactory()
            demandeur_id = uuid4()
        else:
            demandeur, organisme = create_organisme_with_agent(role=role)
            demandeur_id = demandeur.utilisateur_id

        with pytest.raises(AccesOrganismeRefuse):
            can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(demandeur_id),
            )


class TestListerMesRecrutementRbac:
    @pytest.mark.parametrize(
        "role", [AgentOrganismeRole.RESPONSABLE, AgentOrganismeRole.MEMBRE]
    )
    def test_allow_responsable_and_membre(self, db, role):
        agent, organisme = create_organisme_with_agent(role=role)

        result = can_execute(
            action=OrganismeAction.LISTER_MES_RECRUTEMENTS,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

        assert result == role

    @pytest.mark.parametrize("est_staff", [False, True])
    def test_reject_no_role_nor_staff(self, db, est_staff):
        organisme = OrganismeDjangoFactory()

        with pytest.raises(AccesOrganismeRefuse):
            can_execute(
                action=OrganismeAction.LISTER_MES_RECRUTEMENTS,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(uuid4(), is_staff=est_staff),
            )


class TestVoirDetailRecrutementRbac:
    @pytest.mark.parametrize("recrutement_role", list(AgentRecrutementRole))
    def test_membre_with_recrutement_role_is_allowed(self, db, recrutement_role):
        membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        RecrutementAgentDjangoFactory(
            recrutement=recrutement, agent=membre, role=recrutement_role.value
        )

        result = can_execute(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=_utilisateur(membre.utilisateur_id),
        )

        assert result == AgentOrganismeRole.MEMBRE

    def test_responsable_bypasses_recrutement_check(self, db):
        responsable, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)

        result = can_execute(
            action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=_utilisateur(responsable.utilisateur_id),
        )

        assert result == AgentOrganismeRole.RESPONSABLE

    def test_membre_without_recrutement_role_is_denied(self, db):
        membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = RecrutementDjangoFactory(organisme=organisme)

        with pytest.raises(AccesRecrutementRefuse):
            can_execute(
                action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                utilisateur=_utilisateur(membre.utilisateur_id),
            )

    def test_unprovided_recrutement_id_is_denied(self, db):
        membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)

        with pytest.raises(AccesRecrutementInconnu):
            can_execute(
                action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(membre.utilisateur_id),
            )

    def test_staff_without_role_is_denied(self, db):
        membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = RecrutementDjangoFactory(organisme=organisme)

        with pytest.raises(AccesRecrutementRefuse):
            can_execute(
                action=OrganismeAction.VOIR_DETAIL_RECRUTEMENT,
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                utilisateur=_utilisateur(membre.utilisateur_id, is_staff=True),
            )


@pytest.mark.parametrize("action", RECRUTEMENT_ETAPES_ACTIONS)
class TestRecrutementEtapesRbac:
    def test_organisme_responsable_bypasses_recrutement_check(self, db, action):
        responsable, organisme = create_organisme_with_agent(
            role=AgentOrganismeRole.RESPONSABLE
        )
        recrutement = RecrutementDjangoFactory(organisme=organisme)

        result = can_execute(
            action=action,
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=_utilisateur(responsable.utilisateur_id),
        )

        assert result == AgentOrganismeRole.RESPONSABLE

    def test_membre_with_recrutement_responsable_is_allowed(self, db, action):
        membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        RecrutementAgentDjangoFactory(
            recrutement=recrutement,
            agent=membre,
            role=AgentRecrutementRole.RESPONSABLE.value,
        )

        result = can_execute(
            action=action,
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            utilisateur=_utilisateur(membre.utilisateur_id),
        )

        assert result == AgentOrganismeRole.MEMBRE

    @pytest.mark.parametrize(
        "recrutement_role",
        [AgentRecrutementRole.RECRUTEUR, AgentRecrutementRole.CONTRIBUTEUR, None],
    )
    def test_membre_without_recrutement_responsable_is_denied(
        self, db, action, recrutement_role
    ):
        membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)
        recrutement = RecrutementDjangoFactory(organisme=organisme)
        if recrutement_role is not None:
            RecrutementAgentDjangoFactory(
                recrutement=recrutement, agent=membre, role=recrutement_role.value
            )

        with pytest.raises(AccesRecrutementRefuse):
            can_execute(
                action=action,
                organisme_id=organisme.id,
                recrutement_id=recrutement.pk,
                utilisateur=_utilisateur(membre.utilisateur_id),
            )

    def test_unprovided_recrutement_id_is_denied(self, db, action):
        membre, organisme = create_organisme_with_agent(role=AgentOrganismeRole.MEMBRE)

        with pytest.raises(AccesRecrutementInconnu):
            can_execute(
                action=action,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(membre.utilisateur_id),
            )

    def test_staff_without_organisme_role_is_denied(self, db, action):
        organisme = OrganismeDjangoFactory()

        with pytest.raises(AccesOrganismeRefuse):
            can_execute(
                action=action,
                organisme_id=organisme.id,
                recrutement_id=uuid4(),
                utilisateur=_utilisateur(uuid4(), is_staff=True),
            )


def test_raises_when_organisme_not_found(db):
    organisme_id = uuid4()

    with pytest.raises(OrganismeNexistePas):
        can_execute(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=organisme_id,
            utilisateur=_utilisateur(uuid4()),
        )


def test_organisme_guard_runs_before_staff_bypass_and_role_check(db):
    organisme_id = uuid4()

    with pytest.raises(OrganismeNexistePas):
        can_execute(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=organisme_id,
            utilisateur=_utilisateur(uuid4(), is_staff=True),
        )


def test_toute_action_membre_est_classee():
    actions_membre = frozenset(
        action
        for action, roles in _ROLES_REQUIS.items()
        if AgentOrganismeRole.MEMBRE in roles
    )

    assert actions_membre <= (
        _ROLES_RECRUTEMENT_REQUIS.keys() | _SANS_ROLE_RECRUTEMENT_REQUIS
    )


@pytest.mark.parametrize("action", ACTIONS_SANS_ORGANISME)
def test_staff_est_autorise_sans_appel_repository(
    db, action, django_assert_num_queries
):
    with django_assert_num_queries(0):
        result = can_execute(
            action=action,
            utilisateur=_utilisateur(uuid4(), is_staff=True),
        )

    assert result is None


class TestModifierOrganisme:
    def test_staff_est_autorise(self, db):
        organisme = OrganismeDjangoFactory()

        result = can_execute(
            action=OrganismeAction.MODIFIER_ORGANISME,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(uuid4(), is_staff=True),
        )

        assert result is None

    def test_non_staff_est_refuse_apres_verification_existence(self, db):
        organisme = OrganismeDjangoFactory()

        with pytest.raises(OperationOrganismeRefusee):
            can_execute(
                action=OrganismeAction.MODIFIER_ORGANISME,
                organisme_id=organisme.id,
                utilisateur=_utilisateur(uuid4()),
            )

    def test_organisme_inexistant_est_priorise_sur_le_statut_staff(self, db):
        organisme_id = uuid4()

        with pytest.raises(OrganismeNexistePas):
            can_execute(
                action=OrganismeAction.MODIFIER_ORGANISME,
                organisme_id=organisme_id,
                utilisateur=_utilisateur(uuid4(), is_staff=True),
            )


def test_revoked_organisme_agent_is_denied(db):
    # Regression: get_role previously ignored date_revocation, so a
    # revoked organisme-agent's stale role still passed permission checks.
    organisme = OrganismeDjangoFactory()
    revoked_agent = OrganismeAgentDjangoFactory(
        organisme=organisme,
        role=AgentOrganismeRole.RESPONSABLE.value,
        date_revocation=timezone.now(),
    ).agent

    with pytest.raises(AccesOrganismeRefuse):
        can_execute(
            action=OrganismeAction.GET_ORGANISME,
            organisme_id=organisme.id,
            utilisateur=_utilisateur(revoked_agent.utilisateur_id),
        )
