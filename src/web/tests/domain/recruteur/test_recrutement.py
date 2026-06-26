from datetime import datetime, timezone
from uuid import uuid4

import pytest
import time_machine

from domain.recruteur.entities.recrutement import Recrutement
from domain.recruteur.errors.erreur_recrutement import CandidatureDejaPresente
from domain.recruteur.events.recrutement_events import (
    CandidatRecrute,
    CandidatureRecue,
    EtapesAppliquees,
    RecrutementCree,
    ResponsableAjoute,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.recrutement_status import RecrutementStatus
from tests.factories.identite.agent_factory import AgentFactory
from tests.factories.recruteur.organisme_factory import (
    EtapeRecrutementFactory,
    make_etapes_recrutement,
)
from tests.factories.recruteur.recrutement_factory import RecrutementFactory

FROZEN_NOW = datetime(2025, 6, 22, 10, 0, 0, tzinfo=timezone.utc)


@time_machine.travel(FROZEN_NOW)
def test_create_recrutement() -> None:
    offre_id = uuid4()
    organisme_id = uuid4()
    etapes = make_etapes_recrutement()

    recrutement = Recrutement.create(
        offre_id=offre_id,
        organisme_id=organisme_id,
        etapes=etapes,
    )

    events = recrutement.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], RecrutementCree)
    assert recrutement.offre_id == offre_id
    assert recrutement.organisme_id == organisme_id
    assert recrutement.etapes == etapes
    assert recrutement.status == RecrutementStatus.ACTIF
    assert recrutement.positions == ()
    assert recrutement.derniere_activite_le == FROZEN_NOW
    assert recrutement.candidat_recrute_id is None


def test_appliquer_etapes() -> None:
    recrutement = RecrutementFactory.create_entity()
    etapes = (
        EtapeRecrutementFactory.create_entity(
            categorie=CategorieEtapeRecrutement.ENTREE,
            nom="Candidature reçue",
        ),
        EtapeRecrutementFactory.create_entity(
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Présélection",
        ),
    )

    recrutement.appliquer_etapes(etapes=etapes)

    events = recrutement.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], EtapesAppliquees)
    assert events[0].etapes == etapes
    assert recrutement.etapes == etapes
    assert len(recrutement.etapes) == 2  # noqa


def test_ajouter_responsables() -> None:
    recrutement = RecrutementFactory.create_entity()
    responsable1 = AgentFactory.create_entity()
    responsable2 = AgentFactory.create_entity()

    recrutement.ajouter_responsable(agent_id=responsable1.entity_id)
    recrutement.ajouter_responsable(agent_id=responsable2.entity_id)

    events = recrutement.collect_events()
    assert len(events) == 2  # noqa
    assert isinstance(events[0], ResponsableAjoute)
    assert isinstance(events[1], ResponsableAjoute)
    assert recrutement.responsables_ids == (
        responsable1.entity_id,
        responsable2.entity_id,
    )


def test_recevoir_candidature() -> None:
    recrutement = RecrutementFactory.create_entity()
    candidature1_id = uuid4()
    candidature2_id = uuid4()

    recrutement.recevoir_candidature(candidature_id=candidature1_id)
    recrutement.recevoir_candidature(candidature_id=candidature2_id)

    events = recrutement.collect_events()
    assert len(events) == 2  # noqa
    assert all(isinstance(e, CandidatureRecue) for e in events)
    assert recrutement.positions[0].candidature_id == candidature2_id
    assert recrutement.positions[1].candidature_id == candidature1_id


def test_recevoir_candidature_deja_presente() -> None:
    candidature_id = uuid4()
    recrutement = RecrutementFactory.create_entity()
    recrutement.recevoir_candidature(candidature_id=candidature_id)

    with pytest.raises(CandidatureDejaPresente):
        recrutement.recevoir_candidature(candidature_id=candidature_id)


@time_machine.travel(FROZEN_NOW)
def test_recruter_candidat() -> None:
    recrutement = RecrutementFactory.create_entity(
        status=RecrutementStatus.ACTIF, derniere_activite_le=FROZEN_NOW
    )
    candidat_id = uuid4()

    recrutement.recruter_candidat(candidat_id=candidat_id)

    events = recrutement.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], CandidatRecrute)
    assert events[0].candidat_id == candidat_id
    assert recrutement.candidat_recrute_id == candidat_id
    assert recrutement.status == RecrutementStatus.ARCHIVE
    assert recrutement.derniere_activite_le == FROZEN_NOW
