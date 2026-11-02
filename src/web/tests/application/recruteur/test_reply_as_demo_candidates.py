from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from django.utils import timezone

from application.recruteur.services.reply_as_demo_candidates import (
    reply_as_demo_candidates,
)
from domain.commons.services.audit_log_writer import AuditLogWriter
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
    MessageModel,
)
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
    MessageDjangoFactory,
)


def _message(conversation, minutes_ago, **kwargs):
    message = MessageDjangoFactory(conversation=conversation, **kwargs)
    MessageModel.objects.filter(pk=message.pk).update(
        created_at=timezone.now() - timedelta(minutes=minutes_ago)
    )
    return message


def _conversation_with_agent_message(
    email="camille.durand@demo.candidat.fr", minutes_ago=3
):
    conversation = ConversationDjangoFactory(
        candidature__candidat__utilisateur__email=email
    )
    agent_message = _message(conversation, minutes_ago)
    return conversation, agent_message.auteur


@pytest.fixture(autouse=True)
def _two_minutes_delay(settings):
    settings.DEMO_AUTO_REPLY_DELAY_MINUTES = 2


def test_replies_as_the_demo_candidate_to_an_agent_message(db):
    conversation, agent = _conversation_with_agent_message()
    candidat_id = conversation.candidature.candidat_id

    assert reply_as_demo_candidates() == 1

    reply = MessageModel.objects.by_conversation(conversation.pk).last()
    assert reply is not None
    assert (reply.contenu, reply.auteur_id) == (
        (
            "Je suis un candidat fictif. Je réponds à votre message pour que vous "
            "puissiez avoir une expérience complète de l'activité messagerie."
        ),
        candidat_id,
    )
    assert list(
        AuditLogModel.objects.filter(event_name="MessageCree").values_list(
            "utilisateur_id", "ressource_kind", "ressource_id"
        )
    ) == [(candidat_id, "Message", reply.id)]
    assert list(
        ConversationModel.objects.unread_by(agent.username).values_list("pk", flat=True)
    ) == [conversation.pk]


@pytest.mark.parametrize(
    "case", ["too_recent", "last_message_by_the_candidate", "not_a_demo_candidate"]
)
def test_does_not_reply(db, case):
    if case == "too_recent":
        _conversation_with_agent_message(minutes_ago=1)
    elif case == "last_message_by_the_candidate":
        conversation, _ = _conversation_with_agent_message(minutes_ago=5)
        _message(conversation, minutes_ago=3, par_candidat=True)
    else:
        _conversation_with_agent_message(email="camille.durand@candidat.fr")
    messages_before = MessageModel.objects.count()

    assert reply_as_demo_candidates() == 0
    assert MessageModel.objects.count() == messages_before


def test_replies_once_to_several_agent_messages(db):
    conversation, _ = _conversation_with_agent_message(minutes_ago=5)
    _message(conversation, minutes_ago=3)

    assert reply_as_demo_candidates() == 1
    assert (
        MessageModel.objects.filter(
            auteur_id=conversation.candidature.candidat_id
        ).count()
        == 1
    )


def test_does_nothing_in_production(db, monkeypatch):
    monkeypatch.setenv("SCALEWAY_ENV", "prod")
    _conversation_with_agent_message()

    assert reply_as_demo_candidates() == 0
    assert MessageModel.objects.count() == 1


@patch.object(
    AuditLogWriter,
    "log_action",
    new=Mock(side_effect=RuntimeError("audit log write failed")),
)
def test_nothing_is_persisted_when_the_audit_cannot_be_written(db):
    _conversation_with_agent_message()

    with pytest.raises(RuntimeError):
        reply_as_demo_candidates()

    assert MessageModel.objects.count() == 1
