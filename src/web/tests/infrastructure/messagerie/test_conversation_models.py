from datetime import timedelta

import pytest
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.db.models.fetch_modes import FETCH_RAISE
from django.utils import timezone

from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
    MessageDocumentModel,
    MessageModel,
)
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
    first_message = MessageDjangoFactory(conversation=conversation, contenu="Premier")
    last_message = MessageDjangoFactory(conversation=conversation, contenu="Dernier")

    (result,) = (
        ConversationModel.objects.by_candidature(conversation.candidature_id)
        .with_message_summary()
        .fetch_mode(FETCH_RAISE)
    )

    assert result.premiers_messages == [first_message]
    assert result.derniers_messages == [last_message]
    assert result.premiers_messages[0].auteur == first_message.auteur
    assert result.derniers_messages[0].auteur == last_message.auteur
    assert result.last_message_created_at == last_message.created_at


def test_by_candidature_orders_by_last_message_and_skips_empty_conversations(db):
    older = ConversationDjangoFactory(with_message=True)
    newer = ConversationDjangoFactory(candidature=older.candidature, with_message=True)
    ConversationDjangoFactory(candidature=older.candidature)

    result = ConversationModel.objects.by_candidature(
        older.candidature_id
    ).with_message_summary()

    assert list(result) == [newer, older]


def _is_unread(conversation, utilisateur):
    (result,) = (
        ConversationModel.objects.by_candidature(conversation.candidature_id)
        .with_message_summary()
        .with_is_unread(utilisateur.username)
    )
    return result.is_unread


@pytest.mark.parametrize(
    "read_at_offset,expected",
    [
        (None, True),
        (timedelta(minutes=-1), True),
        (timedelta(0), False),
        (timedelta(minutes=1), False),
    ],
    ids=["no_receipt", "older_receipt", "receipt_at_last_message", "newer_receipt"],
)
def test_is_unread_depends_on_the_read_receipt_of_the_viewer(
    db, read_at_offset, expected
):
    message = MessageDjangoFactory()
    viewer = UtilisateurDjangoFactory()
    if read_at_offset is not None:
        ConversationLectureDjangoFactory(
            conversation=message.conversation,
            utilisateur=viewer,
            read_at=message.created_at + read_at_offset,
        )

    assert _is_unread(message.conversation, viewer) is expected


def test_is_unread_ignores_the_read_receipt_of_another_user(db):
    message = MessageDjangoFactory()
    ConversationLectureDjangoFactory(
        conversation=message.conversation,
        read_at=message.created_at + timedelta(minutes=1),
    )

    assert _is_unread(message.conversation, UtilisateurDjangoFactory()) is True


def test_is_read_when_last_message_is_written_by_the_viewer(db):
    message = MessageDjangoFactory()

    assert _is_unread(message.conversation, message.auteur) is False


def test_is_unread_when_viewer_wrote_only_an_older_message(db):
    conversation = ConversationDjangoFactory()
    viewer = UtilisateurDjangoFactory()
    MessageDjangoFactory(conversation=conversation, auteur=viewer)
    MessageDjangoFactory(conversation=conversation)

    assert _is_unread(conversation, viewer) is True


def test_is_unread_for_the_candidate_follows_the_last_message_author(db):
    conversation = ConversationDjangoFactory()
    candidate = conversation.candidature.candidat.utilisateur
    MessageDjangoFactory(conversation=conversation, par_candidat=True)
    assert _is_unread(conversation, candidate) is False

    MessageDjangoFactory(conversation=conversation)
    assert _is_unread(conversation, candidate) is True


def test_is_unread_is_computed_per_conversation(db):
    unread = ConversationDjangoFactory(with_message=True)
    read = ConversationDjangoFactory(candidature=unread.candidature, with_message=True)
    viewer = UtilisateurDjangoFactory()
    ConversationLectureDjangoFactory(conversation=read, utilisateur=viewer)

    results = (
        ConversationModel.objects.by_candidature(unread.candidature_id)
        .with_message_summary()
        .with_is_unread(viewer.username)
    )

    assert {r.pk: r.is_unread for r in results} == {unread.pk: True, read.pk: False}


def test_by_conversation_orders_attachments_by_creation(db):
    message = MessageDjangoFactory()
    attachments = MessageDocumentDjangoFactory.create_batch(3, message=message)
    for age, attachment in enumerate(attachments):
        MessageDocumentModel.objects.filter(pk=attachment.pk).update(
            created_at=timezone.now() - timedelta(days=age)
        )

    (result,) = MessageModel.objects.by_conversation(message.conversation_id)

    assert [pj.pk for pj in result.pieces_jointes.all()] == [
        pj.pk for pj in reversed(attachments)
    ]
