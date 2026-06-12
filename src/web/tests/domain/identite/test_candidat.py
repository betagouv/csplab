from uuid import UUID, uuid4

import pytest
from faker import Faker

from domain.identite.entities.candidat import Candidat
from domain.identite.events.candidat_events import ProfilCandidatCree

fake = Faker()
_FIXED_ID = uuid4()


@pytest.mark.parametrize(
    "entity_id",
    [pytest.param(None, id="generated"), pytest.param(_FIXED_ID, id="provided")],
)
def test_create(entity_id):
    event = ProfilCandidatCree(
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
        linkedin=fake.url(schemes=["https"]),
    )

    candidat = Candidat.create(event, entity_id=entity_id)

    assert isinstance(candidat.entity_id, UUID)
    if entity_id is not None:
        assert candidat.entity_id == entity_id

    events = candidat.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], ProfilCandidatCree)


def test_build():
    entity_id = uuid4()

    candidat = Candidat.build(
        entity_id=entity_id,
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
        linkedin=fake.url(schemes=["https"]),
    )

    assert candidat.entity_id == entity_id
    assert candidat.collect_events() == []
