from uuid import uuid4

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import IntegrityError
from faker import Faker

from application.recruteur.services.reply_conversation import reply_conversation
from domain.candidate.exceptions.document_errors import FichierDeposeIncomplet
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
from infrastructure.django_apps.candidate.enums.type_document import TypeDocument
from infrastructure.django_apps.candidate.models.document import DocumentModel
from infrastructure.django_apps.commons.models import AuditLogModel
from infrastructure.django_apps.messagerie.models import MessageModel
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
    create_recrutement_and_candidature_for_agent,
    create_recrutement_with_candidature,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.messagerie.conversation_django_factory import (
    ConversationDjangoFactory,
)
from tests.utils.message_documents import PDF_BYTES, pdf

fake = Faker("fr_FR")


def _utilisateur(entity_id, **kwargs):
    return UtilisateurFactory.create_entity(entity_id=entity_id, **kwargs)


def test_authorized_agent_replies_in_the_conversation(db):
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    utilisateur = _utilisateur(agent.utilisateur_id, prenom="Camille", nom="Durand")
    conversation_id = ConversationDjangoFactory(candidature=candidature).pk
    content = fake.sentence(nb_words=30)

    message = reply_conversation(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        conversation_id=conversation_id,
        content=content,
        documents=[pdf("convocation.pdf")],
        utilisateur=utilisateur,
    )

    persisted = MessageModel.objects.get(pk=message.pk)
    assert persisted.conversation_id == conversation_id
    assert persisted.contenu == content
    assert persisted.auteur_id == agent.utilisateur_id
    [piece_jointe] = persisted.pieces_jointes.select_related("document")

    document = piece_jointe.document
    assert document.nom_original == "convocation.pdf"
    assert document.type_document == TypeDocument.AUTRE
    assert document.content_type == "application/pdf"
    assert document.taille == len(PDF_BYTES)
    assert document.candidature_id == candidature.pk
    assert document.depose_par_id == agent.utilisateur_id

    audit = AuditLogModel.objects.get(ressource_id=message.pk)
    assert audit.ressource_kind == "Message"
    assert audit.event_name == "MessageCree"
    assert audit.utilisateur_id == agent.utilisateur_id


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
            utilisateur=_utilisateur(agent.utilisateur_id),
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
            utilisateur=_utilisateur(agent.utilisateur_id),
        )

    assert not MessageModel.objects.exists()
    assert not DocumentModel.objects.exists()
    assert not AuditLogModel.objects.filter(event_name="MessageCree").exists()


def _without_organisme_role():
    recrutement, candidature = create_recrutement_with_candidature(
        OrganismeDjangoFactory()
    )
    return (
        recrutement.organisme_id,
        recrutement.pk,
        candidature.pk,
        ConversationDjangoFactory(candidature=candidature).pk,
        _utilisateur(uuid4()),
    )


def _without_recrutement_role():
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent(role=AgentOrganismeRole.AGENT)
    )
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        ConversationDjangoFactory(candidature=candidature).pk,
        _utilisateur(agent.utilisateur_id),
    )


def _unknown_organisme():
    return uuid4(), uuid4(), uuid4(), uuid4(), _utilisateur(uuid4())


def _recrutement_from_another_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    other_recrutement, other_candidature = create_recrutement_with_candidature(
        OrganismeDjangoFactory()
    )
    return (
        organisme.id,
        other_recrutement.pk,
        other_candidature.pk,
        ConversationDjangoFactory(candidature=other_candidature).pk,
        _utilisateur(agent.utilisateur_id),
    )


def _candidature_from_another_recrutement():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, _ = create_recrutement_with_candidature(organisme)
    _, other_candidature = create_recrutement_with_candidature(organisme)
    return (
        organisme.id,
        recrutement.pk,
        other_candidature.pk,
        ConversationDjangoFactory(candidature=other_candidature).pk,
        _utilisateur(agent.utilisateur_id),
    )


def _unknown_conversation():
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent()
    )
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        uuid4(),
        _utilisateur(agent.utilisateur_id),
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
        _utilisateur(agent.utilisateur_id),
    )


@pytest.mark.parametrize(
    "build_args,error",
    [
        (_without_organisme_role, AccesOrganismeRefuse),
        (_without_recrutement_role, AccesRecrutementRefuse),
        (_unknown_organisme, OrganismeNexistePas),
        (_recrutement_from_another_organisme, RecrutementInexistant),
        (_candidature_from_another_recrutement, RecrutementCandidatureInexistante),
        (_unknown_conversation, ConversationInexistante),
        (_conversation_from_another_candidature, ConversationInexistante),
    ],
    ids=[
        "without_organisme_role",
        "without_recrutement_role",
        "unknown_organisme",
        "recrutement_from_another_organisme",
        "candidature_from_another_recrutement",
        "unknown_conversation",
        "conversation_from_another_candidature",
    ],
)
def test_is_denied(db, build_args, error):
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
