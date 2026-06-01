from domain.candidature.entities.candidature import Candidature
from domain.candidature.events.candidature_events import (
    DocumentsDeposes,
    DossierCandidatureCree,
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
    candidature_factory.deposer_documents(DocumentsDeposes(documents=documents))
    events = candidature_factory.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], DocumentsDeposes)
    assert candidature_factory.documents == documents
