import logging
from uuid import uuid4

import pytest
from django.db import transaction
from django.utils import timezone

from application.recruteur.context_services.candidature_agent_service import (
    CandidatureAgentService,
)
from application.recruteur.errors.application_errors_recruteur import (
    CandidatureInaccessible,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
    OperationOrganismeRefusee,
)
from domain.identite.value_objects.permission_action import PermissionAction
from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.recruteur.models.organisme import OrganismeModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    RecrutementDjangoFactory,
)

ACTION = PermissionAction.LIST_NOTES


def _service(organisme_id, recrutement_id, candidature_id, utilisateur):
    return CandidatureAgentService(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        candidature_id=candidature_id,
        utilisateur=utilisateur,
    )


def _unknown_organisme():
    return uuid4(), uuid4(), uuid4(), UtilisateurDjangoFactory()


def _user_without_organisme_role():
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)
    return organisme.id, recrutement.pk, candidature.pk, UtilisateurDjangoFactory()


def _agent_not_member_of_recrutement():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)
    return organisme.id, recrutement.pk, candidature.pk, agent.utilisateur


def _recrutement_of_another_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement = RecrutementDjangoFactory()
    candidature = CandidatureDjangoFactory(etape__recrutement=recrutement)
    return organisme.id, recrutement.pk, candidature.pk, agent.utilisateur


def _candidature_of_another_recrutement():
    agent, organisme, recrutement, _ = create_recrutement_and_candidature_for_agent()
    other = CandidatureDjangoFactory()
    return organisme.id, recrutement.pk, other.pk, agent.utilisateur


class TestCheckAccessible:
    def test_returns_the_organisme_role(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )

        role = _service(
            organisme.id, recrutement.pk, candidature.pk, agent.utilisateur
        ).check_accessible(ACTION)

        assert role == AgentOrganismeRole.SUPERVISEUR

    @pytest.mark.parametrize(
        ("build_args", "cause"),
        [
            pytest.param(_unknown_organisme, OrganismeNexistePas, id="organisme"),
            pytest.param(
                _user_without_organisme_role, AccesOrganismeRefuse, id="organisme_role"
            ),
            pytest.param(
                _agent_not_member_of_recrutement,
                AccesRecrutementRefuse,
                id="recrutement_role",
            ),
            pytest.param(
                _recrutement_of_another_organisme,
                RecrutementInexistant,
                id="recrutement",
            ),
            pytest.param(
                _candidature_of_another_recrutement,
                RecrutementCandidatureInexistante,
                id="candidature",
            ),
        ],
    )
    def test_translates_the_cause_and_keeps_it_chained(
        self, db, caplog, build_args, cause
    ):
        organisme_id, recrutement_id, candidature_id, utilisateur = build_args()

        service = _service(organisme_id, recrutement_id, candidature_id, utilisateur)

        with caplog.at_level(logging.INFO):
            with pytest.raises(CandidatureInaccessible) as raised:
                service.check_accessible(ACTION)

        assert type(raised.value.__cause__) is cause
        assert f"{candidature_id} inaccessible : {cause.__name__}" in caplog.text

    def test_refuses_a_staff_action_without_organisme_role(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        staff = UtilisateurDjangoFactory(is_staff=True)
        service = _service(organisme.id, recrutement.pk, candidature.pk, staff)

        with pytest.raises(CandidatureInaccessible) as raised:
            service.check_accessible(PermissionAction.UPDATE_ORGANISME)

        assert type(raised.value.__cause__) is OperationOrganismeRefusee

    def test_skips_the_candidature_check_on_demand(self, db):
        agent, organisme, recrutement, _ = (
            create_recrutement_and_candidature_for_agent()
        )
        service = _service(organisme.id, recrutement.pk, uuid4(), agent.utilisateur)

        service.check_accessible(ACTION, check_candidature=False)


class TestCheckExists:
    def test_passes_for_a_candidature_of_the_recrutement(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )

        _service(
            organisme.id, recrutement.pk, candidature.pk, agent.utilisateur
        ).check_exists()

    def test_raises_for_a_deleted_organisme(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )
        OrganismeModel.objects.filter(pk=organisme.pk).update(
            supprime_le=timezone.now()
        )

        with pytest.raises(CandidatureInaccessible) as raised:
            _service(
                organisme.id, recrutement.pk, candidature.pk, agent.utilisateur
            ).check_exists()

        assert type(raised.value.__cause__) is OrganismeNexistePas


class TestLockCandidature:
    def test_passes_when_candidature_belongs_to_recrutement(self, db):
        agent, organisme, recrutement, candidature = (
            create_recrutement_and_candidature_for_agent()
        )

        with transaction.atomic():
            _service(
                organisme.id, recrutement.pk, candidature.pk, agent.utilisateur
            ).lock_candidature()

    def test_raises_when_candidature_does_not_exist(self, db):
        agent, organisme, recrutement, _ = (
            create_recrutement_and_candidature_for_agent()
        )
        service = _service(organisme.id, recrutement.pk, uuid4(), agent.utilisateur)

        with transaction.atomic(), pytest.raises(CandidatureInaccessible) as raised:
            service.lock_candidature()

        assert type(raised.value.__cause__) is RecrutementCandidatureInexistante


class TestCheckConversationBelongsToCandidature:
    def test_passes_when_conversation_belongs_to_candidature(self, db):
        conversation = ConversationDjangoFactory()

        _service(
            uuid4(), uuid4(), conversation.candidature_id, UtilisateurDjangoFactory()
        ).check_conversation_belongs_to_candidature(conversation.pk)

    def test_raises_when_conversation_belongs_to_another_candidature(self, db):
        conversation = ConversationDjangoFactory()
        other = CandidatureDjangoFactory()
        service = _service(uuid4(), uuid4(), other.pk, UtilisateurDjangoFactory())

        with pytest.raises(ConversationInexistante):
            service.check_conversation_belongs_to_candidature(conversation.pk)

    def test_raises_when_conversation_does_not_exist(self, db):
        with pytest.raises(ConversationInexistante):
            _service(
                uuid4(), uuid4(), uuid4(), UtilisateurDjangoFactory()
            ).check_conversation_belongs_to_candidature(uuid4())
