from datetime import datetime, timedelta
from io import StringIO

import pytest
from django.core.management import call_command
from django.utils import timezone
from huey.api import PeriodicTask

from infrastructure.django_apps.messagerie.models import MessageModel
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
    MessageDjangoFactory,
)
from presentation.recruteur.tasks import reply_as_demo_candidates_periodic


@pytest.fixture
def conversation_awaiting_reply(db, settings):
    settings.DEMO_AUTO_REPLY_DELAY_MINUTES = 2
    conversation = ConversationDjangoFactory(
        candidature__candidat__utilisateur__email="camille.durand@demo.candidat.fr"
    )
    message = MessageDjangoFactory(conversation=conversation)
    MessageModel.objects.filter(pk=message.pk).update(
        created_at=timezone.now() - timedelta(minutes=3)
    )
    return conversation


def test_periodic_task_runs_every_minute():
    assert issubclass(reply_as_demo_candidates_periodic.task_class, PeriodicTask)

    skipped = [
        (hour, minute)
        for hour in range(24)
        for minute in range(60)
        if not reply_as_demo_candidates_periodic.task_class().validate_datetime(
            datetime(2026, 6, 1, hour, minute)
        )
    ]

    assert skipped == []


def test_periodic_task_replies_as_the_demo_candidate(conversation_awaiting_reply):
    reply_as_demo_candidates_periodic.call_local()

    assert MessageModel.objects.filter(
        conversation=conversation_awaiting_reply,
        auteur_id=conversation_awaiting_reply.candidature.candidat_id,
    ).exists()


def test_command_reports_the_number_of_replies(conversation_awaiting_reply):
    out = StringIO()

    call_command("reply_as_demo_candidates", stdout=out)

    assert out.getvalue() == "1 réponse(s) envoyée(s).\n"
