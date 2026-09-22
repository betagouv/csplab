from uuid import uuid4

import pytest

from application.recruteur.context_services.recrutement_agent_service import (
    RecrutementAgentService,
)
from domain.recruteur.errors.recrutement_errors import RecrutementDocumentInexistant
from infrastructure.factories.candidate.candidature_django_factory import (
    CandidatureDjangoFactory,
)
from infrastructure.factories.candidate.document_django_factory import (
    DocumentDjangoFactory,
)
from infrastructure.factories.identite.organisme_django_factory import (
    OrganismeDjangoFactory,
)
from infrastructure.factories.recruteur.recrutement_django_factory import (
    EtapeDjangoFactory,
    RecrutementDjangoFactory,
)


def test_document_belongs_to_recrutement(db):
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )
    document = DocumentDjangoFactory(candidature=candidature)

    RecrutementAgentService(
        organisme_id=organisme.id, recrutement_id=recrutement.pk
    ).check_document_belongs_to_recrutement(candidature.pk, document.pk)


def test_document_from_another_recrutement_is_denied(db):
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    other_document = DocumentDjangoFactory()  # different, unrelated recrutement

    with pytest.raises(RecrutementDocumentInexistant):
        RecrutementAgentService(
            organisme_id=organisme.id, recrutement_id=recrutement.pk
        ).check_document_belongs_to_recrutement(
            other_document.candidature_id, other_document.pk
        )


def test_document_from_different_candidature_is_denied(db):
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    etape = EtapeDjangoFactory(recrutement=recrutement)
    candidature = CandidatureDjangoFactory(etape=etape)
    other_candidature = CandidatureDjangoFactory(etape=etape)  # same recrutement
    document = DocumentDjangoFactory(candidature=candidature)

    with pytest.raises(RecrutementDocumentInexistant):
        RecrutementAgentService(
            organisme_id=organisme.id, recrutement_id=recrutement.pk
        ).check_document_belongs_to_recrutement(other_candidature.pk, document.pk)


def test_unknown_document_is_denied(db):
    organisme = OrganismeDjangoFactory()
    recrutement = RecrutementDjangoFactory(organisme=organisme)
    candidature = CandidatureDjangoFactory(
        etape=EtapeDjangoFactory(recrutement=recrutement)
    )

    with pytest.raises(RecrutementDocumentInexistant):
        RecrutementAgentService(
            organisme_id=organisme.id, recrutement_id=recrutement.pk
        ).check_document_belongs_to_recrutement(candidature.pk, uuid4())
