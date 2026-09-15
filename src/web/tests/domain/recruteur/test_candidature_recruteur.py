from datetime import datetime, timezone
from uuid import uuid4

import time_machine

from domain.recruteur.events.candidature_events import (
    CandidatureEtapeModifiee,
    CandidatureRecue,
)
from infrastructure.factories.recruteur.candidature_recruteur_factory import (
    CandidatureRecruteurFactory,
)

_FROZEN_TS = datetime.now(tz=timezone.utc)


@time_machine.travel(_FROZEN_TS, tick=False)
def test_candidature_recruteur_recue() -> None:
    recrutement_id = uuid4()
    etape_id = uuid4()
    candidat_id = uuid4()

    candidature = CandidatureRecruteurFactory.create_entity(
        recrutement_id=recrutement_id,
        etape_id=etape_id,
        derniere_activite_le=_FROZEN_TS,
    )
    candidature.recevoir_candidature(etape_id=etape_id, candidat_id=candidat_id)

    events = candidature.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], CandidatureRecue)

    assert candidature.recrutement_id == recrutement_id
    assert candidature.etape_id == etape_id
    assert candidature.derniere_activite_le == _FROZEN_TS
    assert candidature.candidat_id == candidat_id


@time_machine.travel(_FROZEN_TS, tick=False)
def test_candidature_recruteur_changer_etape_avec_motif_refus() -> None:
    etape_id = uuid4()

    candidature = CandidatureRecruteurFactory.create_entity()
    candidature.changer_etape(etape_id=etape_id, motif_refus="autre")

    events = candidature.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], CandidatureEtapeModifiee)
    assert events[0].motif_refus == "autre"

    assert candidature.etape_id == etape_id
    assert candidature.motif_refus == "autre"
