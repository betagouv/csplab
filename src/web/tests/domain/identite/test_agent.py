from uuid import UUID, uuid4

from faker import Faker

from domain.identite.entities.agent import Agent
from domain.identite.events.agent_events import ProfilAgentCree

fake = Faker()


def test_create():
    user_id = uuid4()
    agent = Agent.create(
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        intitule_poste=fake.word(),
        user_id=user_id,
    )

    assert isinstance(agent.entity_id, UUID)
    assert agent.entity_id == user_id

    events = agent.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], ProfilAgentCree)
    assert events[0].user_id == user_id


def test_build():
    entity_id = uuid4()

    agent = Agent.build(
        entity_id=entity_id,
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        intitule_poste=fake.bothify("MAT-####"),
    )

    assert agent.entity_id == entity_id
    assert agent.collect_events() == []
