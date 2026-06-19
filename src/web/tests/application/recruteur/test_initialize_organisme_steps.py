from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from tests.factories.recruteur.organisme_factory import OrganismeRecruteurFactory


def test_initialize_organisme_steps(initialize_organisme_steps_usecase):
    organisme_before = OrganismeRecruteurFactory.create_entity()
    initialize_organisme_steps_usecase.organisme_repository.save(organisme_before)

    organisme = initialize_organisme_steps_usecase.execute(
        command=InitializeOrganismeStepsCommand(organisme_id=organisme_before.entity_id)
    )

    events = organisme.collect_events()
    assert len(events) == 1
