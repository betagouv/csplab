from uuid import uuid4

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from faker import Faker

from application.recruteur.services.reply_conversation import reply_conversation
from domain.candidate.exceptions.document_errors import FichierDeposeIncomplet
from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
)
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.messagerie.models import MessageModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
)
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
)
from tests.utils.message_documents import PDF_BYTES

fake = Faker("fr_FR")


def test_nothing_is_persisted_when_the_message_cannot_be_created(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    conversation_id = ConversationDjangoFactory(candidature=candidature).pk

    with pytest.raises(IntegrityError):
        reply_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=conversation_id,
            content="",
            documents=[],
            utilisateur=agent.utilisateur,
        )

    assert not MessageModel.objects.exists()
    assert not AuditLogModel.objects.filter(event_name="MessageCree").exists()


def test_nothing_is_persisted_when_a_document_is_incomplete(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    incomplete = SimpleUploadedFile("cv.pdf", PDF_BYTES)
    incomplete.content_type = None

    with pytest.raises(FichierDeposeIncomplet):
        reply_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=ConversationDjangoFactory(candidature=candidature).pk,
            content=fake.sentence(nb_words=30),
            documents=[incomplete],
            utilisateur=agent.utilisateur,
        )

    assert not MessageModel.objects.exists()
    assert not DocumentModel.objects.exists()
    assert not AuditLogModel.objects.filter(event_name="MessageCree").exists()


def _unknown_conversation():
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        uuid4(),
        agent.utilisateur,
    )


def _conversation_from_another_candidature():
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    other_candidature = CandidatureDjangoFactory(etape=candidature.etape)
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        ConversationDjangoFactory(candidature=other_candidature).pk,
        agent.utilisateur,
    )


@pytest.mark.parametrize(
    "build_args,error",
    [
        (_unknown_conversation, ConversationInexistante),
        (_conversation_from_another_candidature, ConversationInexistante),
    ],
    ids=[
        "unknown_conversation",
        "conversation_from_another_candidature",
    ],
)
def test_conversation_not_of_the_candidature_is_not_found(db, build_args, error):
    organisme_id, recrutement_id, candidature_id, conversation_id, utilisateur = (
        build_args()
    )

    with pytest.raises(error):
        reply_conversation(
            organisme_id=organisme_id,
            recrutement_id=recrutement_id,
            candidature_id=candidature_id,
            conversation_id=conversation_id,
            content=fake.sentence(nb_words=30),
            documents=[],
            utilisateur=utilisateur,
        )
