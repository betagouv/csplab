from uuid import uuid4

import pytest
from django.db import IntegrityError
from faker import Faker

from application.recruteur.services.create_conversation import create_conversation
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import (
    AccesOrganismeRefuse,
    AccesRecrutementRefuse,
)
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.django_apps.messagerie.models import (
    ConversationModel,
)
from infrastructure.factories.candidate.candidature_django_factory import (
    create_recrutement_and_candidature_for_agent,
    create_recrutement_with_candidature,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
    create_organisme_with_agent,
)
from infrastructure.factories.identite.utilisateur_django_factory import (
    UtilisateurDjangoFactory,
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


def _without_organisme_role():
    recrutement, candidature = create_recrutement_with_candidature(
        OrganismeDjangoFactory()
    )
    return (
        recrutement.organisme_id,
        recrutement.pk,
        candidature.pk,
        UtilisateurDjangoFactory(),
    )


def _without_recrutement_role():
    agent, organisme, recrutement, candidature = (
        create_recrutement_and_candidature_for_agent(role=AgentOrganismeRole.AGENT)
    )
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        agent.utilisateur,
    )


def _unknown_organisme():
    return uuid4(), uuid4(), uuid4(), UtilisateurDjangoFactory()


def _recrutement_from_another_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    other_recrutement, other_candidature = create_recrutement_with_candidature(
        OrganismeDjangoFactory()
    )
    return (
        organisme.id,
        other_recrutement.pk,
        other_candidature.pk,
        agent.utilisateur,
    )


def _candidature_from_another_recrutement():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, _ = create_recrutement_with_candidature(organisme)
    _, other_candidature = create_recrutement_with_candidature(organisme)
    return (
        organisme.id,
        recrutement.pk,
        other_candidature.pk,
        agent.utilisateur,
    )


@pytest.mark.parametrize(
    "build_args,error",
    [
        (_without_organisme_role, AccesOrganismeRefuse),
        (_without_recrutement_role, AccesRecrutementRefuse),
        (_unknown_organisme, OrganismeNexistePas),
        (_recrutement_from_another_organisme, RecrutementInexistant),
        (_candidature_from_another_recrutement, RecrutementCandidatureInexistante),
    ],
    ids=[
        "without_organisme_role",
        "without_recrutement_role",
        "unknown_organisme",
        "recrutement_from_another_organisme",
        "candidature_from_another_recrutement",
    ],
)
def test_is_denied(db, build_args, error):
    organisme_id, recrutement_id, candidature_id, utilisateur = build_args()

    with pytest.raises(error):
        create_conversation(
            organisme_id=organisme_id,
            recrutement_id=recrutement_id,
            candidature_id=candidature_id,
            objet=fake.sentence(nb_words=4),
            content=fake.sentence(nb_words=30),
            documents=[],
            utilisateur=utilisateur,
        )
