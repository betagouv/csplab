from uuid import uuid4

import pytest

from application.recruteur.services.list_documents import list_documents
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.errors.recrutement_errors import (
    RecrutementCandidatureInexistante,
    RecrutementInexistant,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
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


def _utilisateur(entity_id):
    return UtilisateurFactory.create_entity(entity_id=entity_id)


def test_authorized_agent_lists_the_documents(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    document = DocumentDjangoFactory(candidature=candidature)
    autre_candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    DocumentDjangoFactory(candidature=autre_candidature)

    result = list_documents(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        utilisateur=_utilisateur(agent.utilisateur_id),
    )

    assert list(result) == [document]


def test_unauthorized_agent_is_denied(db):
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )

    with pytest.raises(AccesOrganismeRefuse):
        list_documents(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            utilisateur=_utilisateur(uuid4()),
        )


def test_unknown_organisme_is_denied(db):
    with pytest.raises(OrganismeNexistePas):
        list_documents(
            organisme_id=uuid4(),
            recrutement_id=uuid4(),
            candidature_id=uuid4(),
            utilisateur=_utilisateur(uuid4()),
        )


def test_recrutement_not_under_organisme_is_denied(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    other_organisme = OrganismeDjangoFactory()
    other_recrutement = RecrutementDjangoFactory(organisme=other_organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=other_recrutement)
    )

    with pytest.raises(RecrutementInexistant):
        list_documents(
            organisme_id=organisme.id,
            recrutement_id=other_recrutement.pk,
            candidature_id=candidature.pk,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )


def test_mismatched_candidature_is_denied(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    other_recrutement = RecrutementDjangoFactory(organisme=organisme)
    other_candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=other_recrutement)
    )

    with pytest.raises(RecrutementCandidatureInexistante):
        list_documents(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=other_candidature.pk,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )
