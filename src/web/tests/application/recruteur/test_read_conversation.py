from unittest.mock import patch
from uuid import uuid4

import pytest
from django.db import IntegrityError

from application.recruteur.services.read_conversation import read_conversation
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.errors.recrutement_errors import (
    ConversationInexistante,
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.messagerie.models import ConversationLectureModel
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
    ConversationLectureDjangoFactory,
    MessageDjangoFactory,
    MessageDocumentDjangoFactory,
)


def _utilisateur(entity_id):
    return UtilisateurFactory.create_entity(entity_id=entity_id)


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


def _read(agent, organisme, recrutement, candidature, conversation):
    return read_conversation(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        conversation_id=conversation.pk,
        utilisateur=_utilisateur(agent.utilisateur_id),
    )


def test_reading_marks_the_conversation_as_read(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    conversation = ConversationDjangoFactory(candidature=candidature)

    _read(agent, organisme, recrutement, candidature, conversation)

    assert ConversationLectureModel.objects.filter(
        conversation=conversation, utilisateur_id=agent.utilisateur_id
    ).exists()


def test_reading_again_refreshes_the_existing_read_receipt(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    conversation = ConversationDjangoFactory(candidature=candidature)
    lecture = ConversationLectureDjangoFactory(
        conversation=conversation, utilisateur_id=agent.utilisateur_id
    )
    previous = lecture.read_at

    _read(agent, organisme, recrutement, candidature, conversation)

    lecture.refresh_from_db()
    assert lecture.read_at > previous
    lectures = ConversationLectureModel.objects.filter(conversation=conversation)
    assert lectures.count() == 1


def test_reading_does_not_mark_the_conversation_read_for_others(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    conversation = ConversationDjangoFactory(candidature=candidature)

    _read(agent, organisme, recrutement, candidature, conversation)

    assert ConversationLectureModel.objects.count() == 1


def test_failed_read_receipt_does_not_hide_messages(db, caplog):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    conversation = ConversationDjangoFactory(candidature=candidature)
    message = MessageDjangoFactory(conversation=conversation)
    with patch.object(
        ConversationLectureModel.objects,
        "update_or_create",
        side_effect=IntegrityError("boom"),
    ):
        messages = _read(agent, organisme, recrutement, candidature, conversation)

    assert list(messages) == [message]
    assert "Could not mark conversation" in caplog.text


def test_denied_read_leaves_no_read_receipt(db):
    recrutement, candidature = create_recrutement_with_candidature(
        OrganismeDjangoFactory()
    )
    conversation = ConversationDjangoFactory(candidature=candidature)

    with pytest.raises(AccesOrganismeRefuse):
        read_conversation(
            organisme_id=recrutement.organisme_id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=conversation.pk,
            utilisateur=_utilisateur(uuid4()),
        )

    assert not ConversationLectureModel.objects.exists()


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


def test_agent_without_recrutement_role_is_denied(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent(role=AgentOrganismeRole.AGENT)
    )

    with pytest.raises(AccesRecrutementRefuse):
        read_conversation(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            conversation_id=ConversationDjangoFactory(candidature=candidature).pk,
            utilisateur=_utilisateur(agent.utilisateur_id),
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
