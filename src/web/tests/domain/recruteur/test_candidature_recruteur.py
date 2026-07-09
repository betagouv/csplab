from datetime import datetime, timezone
from uuid import uuid4

import time_machine

from domain.recruteur.events.candidature_events import CandidatureRecue
from tests.factories.recruteur.candidature_recruteur_factory import (
    CandidatureRecruteurFactory,
)

_FROZEN_TS = datetime.now(tz=timezone.utc)


@time_machine.travel(_FROZEN_TS, tick=False)
def test_candidature_recruteur_recue() -> None:
    recrutement_id = uuid4()
    etape_id = uuid4()

    candidature = CandidatureRecruteurFactory.create_entity(
        recrutement_id=recrutement_id,
        etape_id=etape_id,
        derniere_activite_le=_FROZEN_TS,
    )
    candidature.recevoir_candidature(etape_id=etape_id)

    events = candidature.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], CandidatureRecue)

    assert candidature.recrutement_id == recrutement_id
    assert candidature.etape_id == etape_id
    assert candidature.derniere_activite_le == _FROZEN_TS
