from datetime import datetime, timezone
from uuid import uuid4

import time_machine

from tests.factories.recruteur.candidature_recruteur_factory import CandidatureFactory

_FROZEN_TS = datetime.now(tz=timezone.utc)


@time_machine.travel(_FROZEN_TS, tick=False)
def test_candidature_recruteur() -> None:
    recrutement_id = uuid4()
    candidat_id = uuid4()
    etapes_id = uuid4()

    candidature = CandidatureFactory.create_entity(
        recrutement_id=recrutement_id,
        candidat_id=candidat_id,
        etapes_id=etapes_id,
        derniere_activite_le=_FROZEN_TS,
    )
    assert candidature.recrutement_id == recrutement_id
    assert candidature.candidat_id == candidat_id
    assert candidature.etapes_id == etapes_id
    assert candidature.derniere_activite_le == _FROZEN_TS
