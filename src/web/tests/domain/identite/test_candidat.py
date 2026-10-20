from uuid import uuid4

from faker import Faker

from domain.identite.entities.candidat import Candidat

fake = Faker()


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
