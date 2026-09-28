from uuid import uuid4

import pytest

from application.recruteur.services.conversation_stubs import (
    _CONVERSATIONS,
    stub_conversation_id,
)
from application.recruteur.services.reply_conversation import reply_conversation
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
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_factory import UtilisateurFactory
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementDjangoFactory,
)
from tests.utils.message_documents import PDF_BYTES, pdf

OBJET = _CONVERSATIONS[0][0]
CONTENT = "Merci, je confirme ma présence."


def _utilisateur(entity_id, **kwargs):
    return UtilisateurFactory.create_entity(entity_id=entity_id, **kwargs)


def _candidature_for(organisme):
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    return recrutement, candidature


def _conversation_of(candidature):
    return stub_conversation_id(candidature.pk, OBJET)


def _reply(
    organisme_id,
    recrutement_id,
    candidature_id,
    conversation_id,
    utilisateur,
    documents=(),
):
    return reply_conversation(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        candidature_id=candidature_id,
        conversation_id=conversation_id,
        content=CONTENT,
        documents=list(documents),
        utilisateur=utilisateur,
    )


def test_authorized_agent_replies_in_the_conversation(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, candidature = _candidature_for(organisme)
    utilisateur = _utilisateur(agent.utilisateur_id, prenom="Camille", nom="Durand")

    message = _reply(
        organisme.id,
        recrutement.pk,
        candidature.pk,
        _conversation_of(candidature),
        utilisateur,
        documents=[pdf("convocation.pdf")],
    )

    assert message.content == CONTENT
    assert message.author == "Camille Durand"
    [document] = message.documents
    assert document.nom == "convocation.pdf"
    assert document.type == TypeDocument.AUTRE
    assert document.content_type == "application/pdf"
    assert document.taille == len(PDF_BYTES)


def _without_organisme_role():
    recrutement, candidature = _candidature_for(OrganismeDjangoFactory())
    return (
        recrutement.organisme_id,
        recrutement.pk,
        candidature.pk,
        _conversation_of(candidature),
        _utilisateur(uuid4()),
    )


def _without_recrutement_role():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement, candidature = _candidature_for(organisme)
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        _conversation_of(candidature),
        _utilisateur(agent.utilisateur_id),
    )


def _unknown_organisme():
    return uuid4(), uuid4(), uuid4(), uuid4(), _utilisateur(uuid4())


def _recrutement_from_another_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    other_recrutement, other_candidature = _candidature_for(OrganismeDjangoFactory())
    return (
        organisme.id,
        other_recrutement.pk,
        other_candidature.pk,
        _conversation_of(other_candidature),
        _utilisateur(agent.utilisateur_id),
    )


def _candidature_from_another_recrutement():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, _ = _candidature_for(organisme)
    _, other_candidature = _candidature_for(organisme)
    return (
        organisme.id,
        recrutement.pk,
        other_candidature.pk,
        _conversation_of(other_candidature),
        _utilisateur(agent.utilisateur_id),
    )


def _unknown_conversation():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, candidature = _candidature_for(organisme)
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        uuid4(),
        _utilisateur(agent.utilisateur_id),
    )


def _conversation_from_another_candidature():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, candidature = _candidature_for(organisme)
    other_candidature = CandidatureDjangoFactory(etape=candidature.etape)
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        _conversation_of(other_candidature),
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
    with pytest.raises(error):
        _reply(*build_args())
