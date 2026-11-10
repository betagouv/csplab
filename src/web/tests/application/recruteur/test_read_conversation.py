from datetime import timedelta
from unittest.mock import patch
from uuid import uuid4

import pytest
from django.db import IntegrityError
from django.utils import timezone

from application.recruteur.services.read_conversation import (
    mark_as_read,
    read_conversation,
)
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
from infrastructure.factories.identite.agent_django_factory import AgentDjangoFactory
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
)
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
    ConversationLectureDjangoFactory,
    MessageDjangoFactory,
    MessageDocumentDjangoFactory,
)


def test_conversation_without_message_is_empty(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )

    messages = read_conversation(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        conversation_id=ConversationDjangoFactory(candidature=candidature).pk,
        utilisateur=agent.utilisateur,
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
        utilisateur=agent.utilisateur,
    )

    with django_assert_num_queries(
        1  # message + its author
        + 1  # documents
    ):
        for message in messages:
            message.auteur.get_full_name()
            [pj.document.nom_original for pj in message.pieces_jointes.all()]


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
            utilisateur=UtilisateurDjangoFactory(),
        )

    assert not ConversationLectureModel.objects.exists()


def test_mark_as_read_never_moves_the_receipt_backwards(db):
    lecture = ConversationLectureDjangoFactory()
    previous = lecture.read_at

    mark_as_read(
        conversation_id=lecture.conversation_id,
        utilisateur=lecture.utilisateur,
        read_up_to=previous - timedelta(minutes=1),
    )

    lecture.refresh_from_db()
    assert lecture.read_at == previous


def test_mark_as_read_only_concerns_the_reader_and_the_conversation(db):
    agent, _, _, candidature = create_recrutement_and_candidature_for_agent()
    conversation = ConversationDjangoFactory(candidature=candidature)
    other_conversation = ConversationDjangoFactory(candidature=candidature)
    other_agent = AgentDjangoFactory()

    mark_as_read(
        conversation_id=conversation.pk,
        utilisateur=agent.utilisateur,
        read_up_to=timezone.now(),
    )

    receipt = ConversationLectureModel.objects.get()
    assert receipt.conversation_id == conversation.pk
    assert receipt.utilisateur_id == agent.utilisateur_id
    assert receipt.utilisateur_id != other_agent.utilisateur_id
    assert receipt.conversation_id != other_conversation.pk


def test_failed_read_receipt_is_logged_and_swallowed(db, caplog):
    conversation = ConversationDjangoFactory()

    with patch.object(
        ConversationLectureModel.objects,
        "get_or_create",
        side_effect=IntegrityError("boom"),
    ):
        mark_as_read(
            conversation_id=conversation.pk,
            utilisateur=UtilisateurDjangoFactory(),
            read_up_to=timezone.now(),
        )

    assert "Could not mark conversation" in caplog.text


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
            utilisateur=UtilisateurDjangoFactory(),
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
            utilisateur=agent.utilisateur,
        )


def test_unknown_organisme_is_denied(db):
    with pytest.raises(OrganismeNexistePas):
        read_conversation(
            organisme_id=uuid4(),
            recrutement_id=uuid4(),
            candidature_id=uuid4(),
            conversation_id=uuid4(),
            utilisateur=UtilisateurDjangoFactory(),
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
            utilisateur=agent.utilisateur,
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
            utilisateur=agent.utilisateur,
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
            utilisateur=agent.utilisateur,
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
            utilisateur=agent.utilisateur,
        )
