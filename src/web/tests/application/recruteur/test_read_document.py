from uuid import uuid4

import factory
import pytest

from application.recruteur.services.read_document import read_document
from domain.commons.errors.organisme_errors import OrganismeNexistePas
from domain.identite.errors.organisme_permission_errors import AccesOrganismeRefuse
from domain.recruteur.errors.recrutement_errors import (
    RecrutementDocumentInexistant,
    RecrutementDocumentTypeNonAutorise,
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


def test_authorized_agent_gets_the_document(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    document = DocumentDjangoFactory(candidature=candidature)

    result = read_document(
        organisme_id=organisme.id,
        recrutement_id=recrutement.pk,
        candidature_id=candidature.pk,
        document_id=document.pk,
        utilisateur=_utilisateur(agent.utilisateur_id),
    )

    assert result.document.pk == document.pk
    assert result.content_type == "application/pdf"


def test_unauthorized_agent_is_denied(db):
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    document = DocumentDjangoFactory(candidature=candidature)

    with pytest.raises(AccesOrganismeRefuse):
        read_document(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            document_id=document.pk,
            utilisateur=_utilisateur(uuid4()),
        )


def test_unknown_organisme_is_denied(db):
    with pytest.raises(OrganismeNexistePas):
        read_document(
            organisme_id=uuid4(),
            recrutement_id=uuid4(),
            candidature_id=uuid4(),
            document_id=uuid4(),
            utilisateur=_utilisateur(uuid4()),
        )


def test_recrutement_not_under_organisme_is_denied(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    other_organisme = OrganismeDjangoFactory()
    other_recrutement = RecrutementDjangoFactory(organisme=other_organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=other_recrutement)
    )
    document = DocumentDjangoFactory(candidature=candidature)

    with pytest.raises(RecrutementInexistant):
        read_document(
            organisme_id=organisme.id,
            recrutement_id=other_recrutement.pk,
            candidature_id=candidature.pk,
            document_id=document.pk,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )


def test_document_with_disallowed_content_type_is_rejected(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    document = DocumentDjangoFactory(
        candidature=candidature,
        fichier=factory.django.FileField(
            filename="test.html", data=b"<script></script>"
        ),
    )

    with pytest.raises(RecrutementDocumentTypeNonAutorise):
        read_document(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=candidature.pk,
            document_id=document.pk,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )


def test_mismatched_candidature_is_denied(db):
    agent, organisme = create_organisme_with_agent(role=AgentOrganismeRole.SUPERVISEUR)
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    etape = EtapeDjangoFactory(recrutement=recrutement)
    candidature = CandidatureDjangoFactory(etape=etape)
    other_candidature = CandidatureDjangoFactory(etape=etape)
    document = DocumentDjangoFactory(candidature=candidature)

    with pytest.raises(RecrutementDocumentInexistant):
        read_document(
            organisme_id=organisme.id,
            recrutement_id=recrutement.pk,
            candidature_id=other_candidature.pk,
            document_id=document.pk,
            utilisateur=_utilisateur(agent.utilisateur_id),
        )
