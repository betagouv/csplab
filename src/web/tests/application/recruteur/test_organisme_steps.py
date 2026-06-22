from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from tests.factories.recruteur.organisme_factory import OrganismeRecruteurFactory


def test_get_organisme_steps(get_organisme_recruteur_usecase):
    organisme_before = OrganismeRecruteurFactory.create_entity()
    get_organisme_recruteur_usecase.organisme_repository.save(organisme_before)

    organisme = get_organisme_recruteur_usecase.execute(
        command=InitializeOrganismeStepsCommand(organisme_id=organisme_before.entity_id)
    )

    events = organisme.collect_events()
    assert len(events) == 0
    assert organisme.entity_id == organisme_before.entity_id


def test_initialize_organisme_steps(initialize_organisme_steps_usecase):
    organisme_before = OrganismeRecruteurFactory.create_entity()
    initialize_organisme_steps_usecase.organisme_repository.save(organisme_before)

    organisme = initialize_organisme_steps_usecase.execute(
        command=InitializeOrganismeStepsCommand(organisme_id=organisme_before.entity_id)
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert events[0].event_name == "OrganismeEtapesInitialises"
