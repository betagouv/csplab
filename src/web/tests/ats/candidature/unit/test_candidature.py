from datetime import datetime

import pytest

from domain.candidature.entities.candidature import Candidature
from domain.candidature.events.candidature_events import (
    CandidatureRetiree,
    CandidatureSoumise,
    DocumentsDeposes,
    DossierCandidatureCree,
)
from domain.candidature.exceptions import (
    CandidatureNePeutEtreRetiree,
    CandidatureNePeutPasEtreSoumise,
    DossierCandidatureInvalide,
)
from domain.candidature.value_objects.statut_candidature import StatutCandidature
from domain.shared.value_objects.etapes_recrutement import (
    CategorieEtapeRecrutement,
    EtapeRecrutement,
)
from tests.ats.candidature.factories.candidature_factory import (
    CandidatureFactory,
    make_documents,
)


def test_dossier_candidature_cree():
    candidature_factory = CandidatureFactory.build()
    candidature = Candidature.create(
        DossierCandidatureCree(
            profil_candidat_id=candidature_factory.profil_candidat_id,
            offre_id=candidature_factory.offre_id,
            etape_courante=candidature_factory._etape_courante,
        )
    )
    events = candidature.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], DossierCandidatureCree)
    assert candidature.statut == candidature_factory.statut
    assert candidature.etape_courante == candidature_factory._etape_courante


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


def test_candidature_ne_peut_pas_etre_soumise():
    candidature_factory = CandidatureFactory.build(
        etape_courante=EtapeRecrutement(
            nom="Clôture du recrutement",
            categorie=CategorieEtapeRecrutement.CLOTURE,
            identifiant="cloture",
        )
    )

    documents = make_documents()
    candidature_factory.deposer_documents(DocumentsDeposes(documents=documents))
    with pytest.raises(CandidatureNePeutPasEtreSoumise):
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
