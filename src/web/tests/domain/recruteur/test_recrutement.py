from datetime import datetime, timezone
from uuid import uuid4

import pytest
import time_machine

from domain.recruteur.errors.recrutement_errors import MotifRefusRequis
from domain.recruteur.value_objects.statut_recrutement import StatutRecrutement
from infrastructure.factories.recruteur.candidature_recruteur_factory import (
    CandidatureRecruteurFactory,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.recrutement_factory import RecrutementFactory

_FROZEN_TS = datetime.now(tz=timezone.utc)


@time_machine.travel(_FROZEN_TS, tick=False)
def test_recrutement() -> None:
    offre_id = uuid4()
    etapes = EtapeRecrutementFactory.create_entity_batch()
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
    etapes = EtapeRecrutementFactory.create_entity_batch()
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


def test_changer_etapes_candidatures_vers_refus_sans_motif() -> None:
    etapes = EtapeRecrutementFactory.create_entity_batch()
    recrutement = RecrutementFactory.create_entity(etapes=etapes)
    etape_refus = etapes[-2]
    candidatures = CandidatureRecruteurFactory.create_entity_batch(
        2, recrutement_id=recrutement.entity_id
    )

    with pytest.raises(MotifRefusRequis):
        recrutement.changer_etapes_candidatures(
            candidatures=candidatures, etape_cible_id=etape_refus.entity_id
        )


def test_changer_etapes_candidatures_vers_refus_avec_motif() -> None:
    etapes = EtapeRecrutementFactory.create_entity_batch()
    recrutement = RecrutementFactory.create_entity(etapes=etapes)
    etape_refus = etapes[-2]
    candidatures = CandidatureRecruteurFactory.create_entity_batch(
        2, recrutement_id=recrutement.entity_id
    )

    resultat = recrutement.changer_etapes_candidatures(
        candidatures=candidatures,
        etape_cible_id=etape_refus.entity_id,
        motif_refus="autre",
    )

    assert resultat["successes"] == candidatures
    assert resultat["failures"] == []


def test_changer_etapes_candidatures_vers_etape_non_refus_sans_motif() -> None:
    etapes = EtapeRecrutementFactory.create_entity_batch()
    recrutement = RecrutementFactory.create_entity(etapes=etapes)
    etape_non_refus = etapes[1]
    candidatures = CandidatureRecruteurFactory.create_entity_batch(
        2, recrutement_id=recrutement.entity_id
    )

    resultat = recrutement.changer_etapes_candidatures(
        candidatures=candidatures, etape_cible_id=etape_non_refus.entity_id
    )

    assert resultat["successes"] == candidatures
    assert resultat["failures"] == []
