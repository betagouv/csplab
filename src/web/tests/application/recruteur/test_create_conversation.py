from uuid import uuid4

import pytest
from django.conf import settings

from application.recruteur.services.create_conversation import create_conversation
from application.recruteur.services.list_conversations import stub_conversation_id
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementDjangoFactory,
)

OBJET = "Convocation à l'entretien"
CONTENT = "Bonjour, pouvez-vous confirmer votre présence ?"


def _utilisateur(entity_id, **kwargs):
    return UtilisateurFactory.create_entity(entity_id=entity_id, **kwargs)


def _candidature_for(organisme):
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    return recrutement, candidature


def _create(organisme_id, recrutement_id, candidature_id, utilisateur, **kwargs):
    return create_conversation(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        candidature_id=candidature_id,
        objet=kwargs.get("objet", OBJET),
        content=kwargs.get("content", CONTENT),
        documents=[],
        utilisateur=utilisateur,
    )


@pytest.fixture
def superviseur_candidature(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, candidature = _candidature_for(organisme)
    return agent, organisme, recrutement, candidature


def test_authorized_agent_creates_a_conversation(superviseur_candidature):
    agent, organisme, recrutement, candidature = superviseur_candidature
    utilisateur = _utilisateur(agent.utilisateur_id, prenom="Camille", nom="Durand")

    conversation = _create(organisme.id, recrutement.pk, candidature.pk, utilisateur)

    assert conversation.uuid == stub_conversation_id(candidature.pk, OBJET)
    assert conversation.objet == OBJET
    assert conversation.creator == "Camille Durand"
    assert conversation.last_message_author == "Camille Durand"
    assert conversation.last_message_content == CONTENT
    assert conversation.created_at == conversation.last_message_created_at


def test_last_message_content_is_truncated(superviseur_candidature):
    agent, organisme, recrutement, candidature = superviseur_candidature

    conversation = _create(
        organisme.id,
        recrutement.pk,
        candidature.pk,
        _utilisateur(agent.utilisateur_id),
        content="a" * (settings.CONVERSATION_LAST_MESSAGE_CONTENT_MAX_LENGTH + 1),
    )

    assert (
        len(conversation.last_message_content)
        == settings.CONVERSATION_LAST_MESSAGE_CONTENT_MAX_LENGTH
    )


def _without_organisme_role():
    recrutement, candidature = _candidature_for(OrganismeDjangoFactory())
    return (
        recrutement.organisme_id,
        recrutement.pk,
        candidature.pk,
        _utilisateur(uuid4()),
    )


def _without_recrutement_role():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement, candidature = _candidature_for(organisme)
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        _utilisateur(agent.utilisateur_id),
    )


def _unknown_organisme():
    return uuid4(), uuid4(), uuid4(), _utilisateur(uuid4())


def _recrutement_from_another_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    other_recrutement, other_candidature = _candidature_for(OrganismeDjangoFactory())
    return (
        organisme.id,
        other_recrutement.pk,
        other_candidature.pk,
        _utilisateur(agent.utilisateur_id),
    )


def _candidature_from_another_recrutement():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, _ = _candidature_for(organisme)
    _, other_candidature = _candidature_for(organisme)
    return (
        organisme.id,
        recrutement.pk,
        other_candidature.pk,
        _utilisateur(agent.utilisateur_id),
    )


@pytest.mark.parametrize(
    "build_args,error",
    [
        (_without_organisme_role, AccesOrganismeRefuse),
        (_without_recrutement_role, AccesRecrutementRefuse),
        (_unknown_organisme, OrganismeNexistePas),
        (_recrutement_from_another_organisme, RecrutementInexistant),
        (_candidature_from_another_recrutement, RecrutementCandidatureInexistante),
    ],
    ids=[
        "without_organisme_role",
        "without_recrutement_role",
        "unknown_organisme",
        "recrutement_from_another_organisme",
        "candidature_from_another_recrutement",
    ],
)
def test_is_denied(db, build_args, error):
    with pytest.raises(error):
        _create(*build_args())
