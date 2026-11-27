import pytest
from django.db import IntegrityError
from faker import Faker

from application.recruteur.services.create_conversation import create_conversation
from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_and_candidature_for_agent,
)

fake = Faker("fr_FR")


def test_nothing_is_persisted_when_the_message_cannot_be_created(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )

    with pytest.raises(IntegrityError):
        create_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            objet=fake.sentence(nb_words=4),
            content="",
            documents=[],
            utilisateur=agent.utilisateur,
        )

    assert not ConversationModel.objects.exists()


def test_created_conversation_is_read_for_its_author(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )

    conversation = create_conversation(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        objet=fake.sentence(nb_words=4),
        content=fake.sentence(),
        documents=[],
        utilisateur=agent.utilisateur,
    )

    assert conversation.is_unread is False
