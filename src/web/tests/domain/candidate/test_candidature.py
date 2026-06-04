from datetime import datetime

import pytest

from domain.candidate.entities.candidature import Candidature
from domain.candidate.events.candidature_events import (
    CandidatureRetiree,
    CandidatureSoumise,
    DocumentsDeposes,
    DossierCandidatureCree,
)
from domain.candidate.exceptions.candidature_errors import (
    CandidatureNePeutEtreRetiree,
    DossierCandidatureInvalide,
)
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from tests.factories.candidate.candidature_factory import (
    CandidatureFactory,
    make_documents,
)


def test_dossier_candidature_cree():
    candidature_factory = CandidatureFactory.build()
    candidature = Candidature.create(
        DossierCandidatureCree(
            profil_candidat_id=candidature_factory.profil_candidat_id,
            offre_id=candidature_factory.offre_id,
        )
    )
    events = candidature.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], DossierCandidatureCree)
    assert candidature.statut == candidature_factory.statut


def test_documents_deposes():
    documents = make_documents()
    candidature_factory = CandidatureFactory.build(documents=documents)
    ts = datetime.now()
    candidature_factory.deposer_documents(
        DocumentsDeposes(documents=documents, occurred_at=ts)
    )
    events = candidature_factory.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], DocumentsDeposes)
    assert candidature_factory.documents == documents
    assert candidature_factory.mise_a_jour_le == ts


def test_candidature_invalide():
    candidature_factory = CandidatureFactory.build()
    with pytest.raises(DossierCandidatureInvalide):
        candidature_factory.deposer_documents(DocumentsDeposes(documents=()))


def test_candidature_soumise():
    candidature_factory = CandidatureFactory.build()
    documents = make_documents()
    candidature_factory.deposer_documents(DocumentsDeposes(documents=documents))
    ts = datetime.now()
    candidature_factory.soumettre_candidature(
        CandidatureSoumise(
            occurred_at=ts,
        )
    )
    events = candidature_factory.collect_events()
    assert len(events) == 2  # noqa
    assert isinstance(events[1], CandidatureSoumise)
    assert candidature_factory.statut == StatutCandidature.SOUMISE
    assert candidature_factory.soumise_le == ts


def test_candidature_soumise_dossier_invalide():
    candidature_factory = CandidatureFactory.build()
    with pytest.raises(DossierCandidatureInvalide):
        candidature_factory.soumettre_candidature(CandidatureSoumise())


def test_candidature_retiree():
    candidature_factory = CandidatureFactory.build(
        statut=StatutCandidature.SOUMISE,
    )
    ts = datetime.now()
    candidature_factory.retirer_candidature(
        CandidatureRetiree(
            occurred_at=ts,
        )
    )
    events = candidature_factory.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], CandidatureRetiree)
    assert candidature_factory.statut == StatutCandidature.RETIREE
    assert candidature_factory.mise_a_jour_le == ts


def test_candidature_ne_peut_pas_etre_retiree():
    candidature_factory = CandidatureFactory.build(
        statut=StatutCandidature.INITIAL,
    )
    with pytest.raises(CandidatureNePeutEtreRetiree):
        candidature_factory.retirer_candidature(CandidatureRetiree())
