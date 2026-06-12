from uuid import UUID, uuid4

import pytest
from faker import Faker

from domain.identite.entities.agent import Agent
from domain.identite.events.agent_events import ProfilAgentCree

fake = Faker()
_FIXED_ID = uuid4()


@pytest.mark.parametrize(
    "entity_id",
    [pytest.param(None, id="generated"), pytest.param(_FIXED_ID, id="provided")],
)
def test_create(entity_id):
    event = ProfilAgentCree(
        email=fake.email(),
        prenom=fake.first_name(),
        nom=fake.last_name(),
        intitule_poste=fake.word(),
    )

    agent = Agent.create(event, entity_id=entity_id)

    assert isinstance(agent.entity_id, UUID)
    if entity_id is not None:
        assert agent.entity_id == entity_id

    events = agent.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], ProfilAgentCree)


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
