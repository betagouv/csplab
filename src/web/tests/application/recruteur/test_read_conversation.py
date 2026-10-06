from uuid import uuid4

import pytest

from application.recruteur.services.read_conversation import read_conversation
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
    create_recrutement_with_candidature,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
    MessageDjangoFactory,
    MessageDocumentDjangoFactory,
)


def _utilisateur(entity_id):
    return UtilisateurFactory.create_entity(entity_id=entity_id)


def test_authorized_agent_reads_the_conversation(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    first = MessageDjangoFactory(
        conversation__candidature=candidature, with_document=True
    )
    conversation = first.conversation
    second = MessageDjangoFactory(conversation=conversation)
    MessageDjangoFactory(conversation__candidature=candidature)

    first_read, second_read = read_conversation(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        conversation_id=conversation.pk,
        utilisateur=_utilisateur(agent.utilisateur_id),
    )

    assert (first_read.pk, second_read.pk) == (first.pk, second.pk)
    assert first_read.pieces_jointes.count() == 1
    assert second_read.pieces_jointes.count() == 0


def test_conversation_without_message_is_empty(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )

    messages = read_conversation(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        conversation_id=ConversationDjangoFactory(candidature=candidature).pk,
        utilisateur=_utilisateur(agent.utilisateur_id),
    )

    assert not messages.exists()


def test_reading_does_not_issue_a_query_per_message(db, django_assert_num_queries):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    conversation = ConversationDjangoFactory(candidature=candidature)
    for message in MessageDjangoFactory.create_batch(2, conversation=conversation):
        MessageDocumentDjangoFactory.create_batch(2, message=message)
    messages = read_conversation(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        conversation_id=conversation.pk,
        utilisateur=_utilisateur(agent.utilisateur_id),
    )

    with django_assert_num_queries(
        1  # message + its author
        + 1  # documents
    ):
        for message in messages:
            message.auteur.get_full_name()
            [pj.document.nom_original for pj in message.pieces_jointes.all()]


def test_unauthorized_agent_is_denied(db):
    recrutement, candidature = create_recrutement_with_candidature(
        OrganismeDjangoFactory()
    )

    with pytest.raises(AccesOrganismeRefuse):
        read_conversation(
            organisme_id=recrutement.organisme_id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=ConversationDjangoFactory(candidature=candidature).pk,
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


def test_recrutement_not_under_organisme_is_denied(db):
    agent, organisme, _, _ = create_recrutement_and_candidature_for_agent()
    other_recrutement, other_candidature = create_recrutement_with_candidature(
        OrganismeDjangoFactory()
    )

    with pytest.raises(RecrutementInexistant):
        read_conversation(
            organisme_id=organisme.id,
            recrutement_id=other_recrutement.pk,
            candidature_id=other_candidature.pk,
            conversation_id=ConversationDjangoFactory(candidature=other_candidature).pk,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )


def test_candidature_not_under_recrutement_is_denied(db):
    agent, organisme, recrutement, _ = create_recrutement_and_candidature_for_agent()
    _, other_candidature = create_recrutement_with_candidature(organisme)

    with pytest.raises(RecrutementCandidatureInexistante):
        read_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=other_candidature.pk,
            conversation_id=ConversationDjangoFactory(candidature=other_candidature).pk,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )


def test_unknown_conversation_is_denied(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )

    with pytest.raises(ConversationInexistante):
        read_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=uuid4(),
            utilisateur=_utilisateur(agent.utilisateur_id),
        )


def test_conversation_of_another_candidature_is_denied(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    other_candidature = CandidatureDjangoFactory(etape=candidature.etape)

    with pytest.raises(ConversationInexistante):
        read_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=ConversationDjangoFactory(candidature=other_candidature).pk,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )
