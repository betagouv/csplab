from uuid import uuid4

import pytest

from application.recruteur.services.list_conversations import (
    _CONVERSATIONS,
    stub_conversation_id,
)
from application.recruteur.services.read_conversation import (
    _MESSAGES,
    MAX_DOCUMENTS_PAR_MESSAGE,
    read_conversation,
)
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
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

OBJET = _CONVERSATIONS[0][0]


def _utilisateur(entity_id):
    return UtilisateurFactory.create_entity(entity_id=entity_id)


def _candidature_for(organisme):
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    return recrutement, candidature


@pytest.fixture
def superviseur_candidature(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, candidature = _candidature_for(organisme)
    return agent, organisme, recrutement, candidature


def test_authorized_agent_reads_the_conversation(superviseur_candidature):
    agent, organisme, recrutement, candidature = superviseur_candidature

    messages = read_conversation(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        conversation_id=stub_conversation_id(candidature.pk, OBJET),
        utilisateur=_utilisateur(agent.utilisateur_id),
    )

    assert len(messages) == len(_MESSAGES)
    dates = [message.created_at for message in messages]
    assert dates == sorted(dates)
    assert all(
        len(message.documents) <= MAX_DOCUMENTS_PAR_MESSAGE for message in messages
    )
    assert any(
        len(message.documents) == MAX_DOCUMENTS_PAR_MESSAGE for message in messages
    )


def test_unauthorized_agent_is_denied(db):
    recrutement, candidature = _candidature_for(OrganismeDjangoFactory())

    with pytest.raises(AccesOrganismeRefuse):
        read_conversation(
            organisme_id=recrutement.organisme_id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=stub_conversation_id(candidature.pk, OBJET),
            utilisateur=_utilisateur(uuid4()),
        )


def test_unknown_organisme_is_denied(db):
    with pytest.raises(OrganismeNexistePas):
        read_conversation(
            organisme_id=uuid4(),
            recrutement_id=uuid4(),
            candidature_id=uuid4(),
            conversation_id=uuid4(),
            utilisateur=_utilisateur(uuid4()),
        )


def test_recrutement_not_under_organisme_is_denied(superviseur_candidature):
    agent, organisme, _, _ = superviseur_candidature
    other_recrutement, other_candidature = _candidature_for(OrganismeDjangoFactory())

    with pytest.raises(RecrutementInexistant):
        read_conversation(
            organisme_id=organisme.id,
            recrutement_id=other_recrutement.pk,
            candidature_id=other_candidature.pk,
            conversation_id=stub_conversation_id(other_candidature.pk, OBJET),
            utilisateur=_utilisateur(agent.utilisateur_id),
        )


def test_candidature_not_under_recrutement_is_denied(superviseur_candidature):
    agent, organisme, recrutement, _ = superviseur_candidature
    _, other_candidature = _candidature_for(organisme)

    with pytest.raises(RecrutementCandidatureInexistante):
        read_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=other_candidature.pk,
            conversation_id=stub_conversation_id(other_candidature.pk, OBJET),
            utilisateur=_utilisateur(agent.utilisateur_id),
        )


def test_unknown_conversation_is_denied(superviseur_candidature):
    agent, organisme, recrutement, candidature = superviseur_candidature

    with pytest.raises(ConversationInexistante):
        read_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=uuid4(),
            utilisateur=_utilisateur(agent.utilisateur_id),
        )


def test_conversation_of_another_candidature_is_denied(superviseur_candidature):
    agent, organisme, recrutement, candidature = superviseur_candidature
    other_candidature = CandidatureDjangoFactory(etape=candidature.etape)

    with pytest.raises(ConversationInexistante):
        read_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=stub_conversation_id(other_candidature.pk, OBJET),
            utilisateur=_utilisateur(agent.utilisateur_id),
        )
