from uuid import UUID, uuid4

from faker import Faker

from domain.identite.entities.candidat import Candidat
from domain.identite.events.candidat_events import ProfilCandidatCree

fake = Faker()


def test_create():
    user_id = uuid4()
    candidat = Candidat.create(
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
        user_id=user_id,
    )

    assert isinstance(candidat.entity_id, UUID)
    assert candidat.entity_id == user_id

    events = candidat.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], ProfilCandidatCree)
    assert events[0].user_id == user_id


def test_build():
    entity_id = uuid4()

    candidat = Candidat.build(
        entity_id=entity_id,
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        resume=fake.text(max_nb_chars=200),
    )

    assert candidat.entity_id == entity_id
    assert candidat.collect_events() == []
