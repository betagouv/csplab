from datetime import datetime, timezone
from uuid import uuid4

import time_machine

from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from tests.factories.recruteur.etapes_recrutement_factory import EtapeRecrutementFactory
from tests.factories.recruteur.recrutement_factory import RecrutementFactory

_FROZEN_TS = datetime.now(tz=timezone.utc)


@time_machine.travel(_FROZEN_TS, tick=False)
def test_recrutement() -> None:
    offre_id = uuid4()
    etapes = EtapeRecrutementFactory.create_entities()
    candidatures = (uuid4(), uuid4(), uuid4())
    agents = (uuid4(), uuid4())

    recrutement = RecrutementFactory.create_entity(
        derniere_activite_le=_FROZEN_TS,
        offre_id=offre_id,
        organisme_id=uuid4(),
        etapes=etapes,
        candidatures=candidatures,
        agents=agents,
        status=StatutRecrutement.ACTIF,
        candidat_recrute_id=None,
    )
    assert recrutement.offre_id == offre_id
    assert recrutement.etapes == etapes
    assert recrutement.candidatures == candidatures
    assert recrutement.status == StatutRecrutement.ACTIF
    assert recrutement.agents == agents
    assert recrutement.candidat_recrute_id is None
    assert recrutement.derniere_activite_le == _FROZEN_TS


@time_machine.travel(_FROZEN_TS, tick=False)
def test_recrutement_termine() -> None:
    offre_id = uuid4()
    etapes = EtapeRecrutementFactory.create_entities()
    candidatures = (uuid4(), uuid4(), uuid4())
    agents = (uuid4(), uuid4())
    candidat_recrute_id = uuid4()

    recrutement = RecrutementFactory.create_entity(
        derniere_activite_le=_FROZEN_TS,
        offre_id=offre_id,
        organisme_id=uuid4(),
        etapes=etapes,
        candidatures=candidatures,
        agents=agents,
        status=StatutRecrutement.ARCHIVE,
        candidat_recrute_id=candidat_recrute_id,
    )
    assert recrutement.offre_id == offre_id
    assert recrutement.etapes == etapes
    assert recrutement.candidatures == candidatures
    assert recrutement.status == StatutRecrutement.ARCHIVE
    assert recrutement.agents == agents
    assert recrutement.candidat_recrute_id == candidat_recrute_id
    assert recrutement.derniere_activite_le == _FROZEN_TS
