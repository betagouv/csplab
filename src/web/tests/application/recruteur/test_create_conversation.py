from uuid import uuid4

import pytest
from django.db import IntegrityError

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

OBJET = "Convocation à l'entretien"
CONTENT = "Bonjour, pouvez-vous confirmer votre présence ?"


def _utilisateur(entity_id, **kwargs):
    return UtilisateurFactory.create_entity(entity_id=entity_id, **kwargs)


def _candidature_for(organisme):
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    return recrutement, candidature


def _create(organisme_id, recrutement_id, candidature_id, utilisateur, **kwargs):
    return create_conversation(
        organisme_id=organisme_id,
        recrutement_id=recrutement_id,
        candidature_id=candidature_id,
        objet=kwargs.get("objet", OBJET),
        content=kwargs.get("content", CONTENT),
        documents=[],
        utilisateur=utilisateur,
    )


@pytest.fixture
def superviseur_candidature(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement, candidature = _candidature_for(organisme)
    return agent, organisme, recrutement, candidature


def test_nothing_is_persisted_when_the_message_cannot_be_created(
    superviseur_candidature,
):
    agent, organisme, recrutement, candidature = superviseur_candidature

    with pytest.raises(IntegrityError):
        _create(
            organisme.id,
            recrutement.pk,
            candidature.pk,
            _utilisateur(agent.utilisateur_id),
            content="",
        )

    assert not ConversationModel.objects.exists()


def _without_organisme_role():
    recrutement, candidature = _candidature_for(OrganismeDjangoFactory())
    return (
        recrutement.organisme_id,
        recrutement.pk,
        candidature.pk,
        _utilisateur(uuid4()),
    )


def _without_recrutement_role():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.AGENT)
    recrutement, candidature = _candidature_for(organisme)
    return (
        organisme.id,
        recrutement.pk,
        candidature.pk,
        _utilisateur(agent.utilisateur_id),
    )


def _unknown_organisme():
    return uuid4(), uuid4(), uuid4(), _utilisateur(uuid4())


def _recrutement_from_another_organisme():
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    other_recrutement, other_candidature = _candidature_for(OrganismeDjangoFactory())
    return (
        organisme.id,
        other_recrutement.pk,
        other_candidature.pk,
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
    with pytest.raises(error):
        _create(*build_args())
