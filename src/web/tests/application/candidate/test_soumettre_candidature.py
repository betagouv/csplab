import pytest

from application.candidate.commands.soumettre_candidature_command import (
    SoumettreCandidatureCommand,
)
from domain.candidate.events.candidature_events import (
    CandidatureSoumise,
    DossierCandidatureInitialise,
)
from domain.candidate.exceptions.candidature_errors import (
    CandidatureDejaSoumise,
    CandidatureNexistePas,
)
from domain.candidate.value_objects.statut_candidature import StatutCandidature
from tests.factories.candidate.candidature_factory import CandidatureFactory


def test_soumettre_candidature_success(soumettre_candidature_usecase):
    factory = CandidatureFactory.build()
    soumettre_candidature_usecase.candidature_repository.get_by_offer.side_effect = (
        CandidatureNexistePas(factory.candidat_id, factory.offre_id)
    )

    candidature = soumettre_candidature_usecase.execute(
        command=SoumettreCandidatureCommand(
            offre_id=factory.offre_id, candidat_id=factory.candidat_id
        )
    )

    events = candidature.collect_events()
    assert len(events) == 2  # noqa
    assert isinstance(events[0], DossierCandidatureInitialise)
    assert isinstance(events[1], CandidatureSoumise)
    assert candidature.statut == StatutCandidature.SOUMISE


def test_echec_soumettre_candidature(soumettre_candidature_usecase):
    existing = CandidatureFactory.build(statut=StatutCandidature.SOUMISE)
    soumettre_candidature_usecase.candidature_repository.get_by_offer.return_value = (
        existing
    )

    with pytest.raises(CandidatureDejaSoumise):
        candidature = soumettre_candidature_usecase.execute(
            command=SoumettreCandidatureCommand(
                offre_id=existing.offre_id, candidat_id=existing.candidat_id
            )
        )
        events = candidature.collect_events()
        assert len(events) == 0
