from datetime import datetime, timezone

import pytest
import time_machine

from domain.candidate.entities.candidature import Candidature
from domain.candidate.events.candidature_events import (
    CandidatureSoumise,
    DocumentsDeposes,
    DossierCandidatureInitialise,
)
from domain.candidate.exceptions.candidature_errors import (
    CandidatureDejaSoumise,
    DossierCandidatureInvalide,
)
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from tests.factories.candidate.candidature_factory import (
    CandidatureFactory,
    make_documents,
)

_FROZEN_TS = datetime.now(tz=timezone.utc)


def test_dossier_candidature_cree():
    candidature_factory = CandidatureFactory.create_entity()
    candidature = Candidature.create(
        offre_id=candidature_factory.offre_id,
        candidat_id=candidature_factory.candidat_id,
    )
    events = candidature.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], DossierCandidatureInitialise)
    assert candidature.statut == StatutCandidature.INITIAL


@time_machine.travel(_FROZEN_TS, tick=False)
def test_documents_deposes():
    documents = make_documents()
    candidature_factory = CandidatureFactory.create_entity(documents=documents)
    candidature_factory.deposer_documents(documents=documents)
    events = candidature_factory.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], DocumentsDeposes)
    assert candidature_factory.documents == documents
    assert candidature_factory.mise_a_jour_le == _FROZEN_TS


def test_candidature_invalide():
    candidature_factory = CandidatureFactory.create_entity()
    with pytest.raises(DossierCandidatureInvalide):
        candidature_factory.deposer_documents(documents=())
    events = candidature_factory.collect_events()
    assert len(events) == 0


@time_machine.travel(_FROZEN_TS, tick=False)
def test_candidature_soumise():
    candidature_factory = CandidatureFactory.create_entity()
    documents = make_documents()
    candidature_factory.deposer_documents(documents=documents)
    candidature_factory.soumettre_candidature()
    events = candidature_factory.collect_events()
    assert len(events) == 2  # noqa
    assert isinstance(events[1], CandidatureSoumise)
    assert candidature_factory.statut == StatutCandidature.SOUMISE
    assert candidature_factory.soumise_le == _FROZEN_TS
    assert candidature_factory.mise_a_jour_le == _FROZEN_TS


def test_candidature_deja_soumise():
    candidature_factory = CandidatureFactory.create_entity(
        statut=StatutCandidature.SOUMISE
    )
    with pytest.raises(CandidatureDejaSoumise):
        candidature_factory.soumettre_candidature()
    events = candidature_factory.collect_events()
    assert len(events) == 0
