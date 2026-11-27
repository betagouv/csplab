import factory
import pytest

from application.recruteur.services.read_document import read_document
from domain.recruteur.errors.recrutement_errors import (
    RecrutementDocumentInexistant,
    RecrutementDocumentTypeNonAutorise,
)
from domain.recruteur.value_objects.roles import AgentOrganismeRole
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    create_organisme_with_agent,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementDjangoFactory,
)


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
        utilisateur=agent.utilisateur,
    )

    assert result.document.pk == document.pk
    assert result.content_type == "application/pdf"


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
            utilisateur=agent.utilisateur,
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
            utilisateur=agent.utilisateur,
        )
