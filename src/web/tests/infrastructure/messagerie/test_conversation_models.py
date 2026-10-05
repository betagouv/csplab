import pytest
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.db.models.fetch_modes import FETCH_RAISE

from infrastructure.django_apps.messagerie.models import ConversationModel
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
    ConversationLectureDjangoFactory,
    MessageDjangoFactory,
    MessageDocumentDjangoFactory,
)


def test_message_written_by_an_agent_or_the_candidate(db):
    conversation = ConversationDjangoFactory()

    agent_message = MessageDjangoFactory(conversation=conversation)
    candidate_message = MessageDjangoFactory(
        conversation=conversation, par_candidat=True
    )

    assert agent_message.auteur != candidate_message.auteur
    assert candidate_message.auteur == conversation.candidature.candidat.utilisateur
    assert set(conversation.messages.all()) == {agent_message, candidate_message}


def test_message_author_cannot_be_deleted(db):
    author = UtilisateurDjangoFactory()
    MessageDjangoFactory(auteur=author)

    with pytest.raises(ProtectedError):
        author.delete()


def test_candidature_with_conversation_cannot_be_deleted(db):
    conversation = ConversationDjangoFactory()

    with pytest.raises(ProtectedError):
        conversation.candidature.delete()


def test_message_with_attached_document_cannot_be_deleted(db):
    attachment = MessageDocumentDjangoFactory(message=MessageDjangoFactory())

    assert (
        attachment.document.candidature == attachment.message.conversation.candidature
    )
    with pytest.raises(ProtectedError):
        attachment.message.delete()


def test_document_can_be_attached_to_a_single_message(db):
    attachment = MessageDocumentDjangoFactory(message=MessageDjangoFactory())

    with pytest.raises(IntegrityError), transaction.atomic():
        MessageDocumentDjangoFactory(
            message=MessageDjangoFactory(), document=attachment.document
        )


def test_empty_message_content_or_conversation_object_is_rejected(db):
    with pytest.raises(IntegrityError), transaction.atomic():
        MessageDjangoFactory(contenu="")
    with pytest.raises(IntegrityError), transaction.atomic():
        ConversationDjangoFactory(objet="")


def test_single_read_receipt_per_user_and_conversation(db):
    read_receipt = ConversationLectureDjangoFactory()

    with pytest.raises(IntegrityError), transaction.atomic():
        ConversationLectureDjangoFactory(
            conversation=read_receipt.conversation, utilisateur=read_receipt.utilisateur
        )


def test_read_receipts_by_agents_and_candidate(db):
    conversation = ConversationDjangoFactory()
    other_agent = AgentDjangoFactory()
    candidate = conversation.candidature.candidat.utilisateur

    agent = AgentDjangoFactory()
    ConversationLectureDjangoFactory(
        conversation=conversation, utilisateur=agent.utilisateur
    )
    ConversationLectureDjangoFactory(
        conversation=conversation, utilisateur=other_agent.utilisateur
    )
    ConversationLectureDjangoFactory(conversation=conversation, utilisateur=candidate)

    assert {
        read_receipt.utilisateur for read_receipt in conversation.lectures.all()
    } == {
        agent.utilisateur,
        other_agent.utilisateur,
        candidate,
    }


def test_by_candidature_prefetches_first_and_last_message_with_their_author(db):
    conversation = ConversationDjangoFactory()
    premier = MessageDjangoFactory(conversation=conversation, contenu="Premier")
    dernier = MessageDjangoFactory(conversation=conversation, contenu="Dernier")

    (result,) = ConversationModel.objects.by_candidature(
        conversation.candidature_id
    ).fetch_mode(FETCH_RAISE)

    assert result.premiers_messages == [premier]
    assert result.derniers_messages == [dernier]
    assert result.premiers_messages[0].auteur == premier.auteur
    assert result.derniers_messages[0].auteur == dernier.auteur
    assert result.last_message_created_at == dernier.created_at


def test_by_candidature_orders_by_last_message_and_skips_empty_conversations(db):
    ancienne = ConversationDjangoFactory()
    recente = ConversationDjangoFactory(candidature=ancienne.candidature)
    ConversationDjangoFactory(candidature=ancienne.candidature)
    MessageDjangoFactory(conversation=ancienne)
    MessageDjangoFactory(conversation=recente)

    result = ConversationModel.objects.by_candidature(ancienne.candidature_id)

    assert list(result) == [recente, ancienne]
