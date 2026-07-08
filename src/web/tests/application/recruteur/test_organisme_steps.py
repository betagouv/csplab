from uuid import uuid4

from application.recruteur.usecases.initialize_organisme_steps import (
    InitializeOrganismeStepsCommand,
)
from application.recruteur.usecases.update_organisme_steps import (
    UpdateOrganismeStepsCommand,
)
from tests.factories.recruteur.etapes_recrutement_factory import EtapeRecrutementFactory
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


def test_update_organsime_steps(update_organisme_steps_usecase):
    etapes = EtapeRecrutementFactory.create_entities()
    organisme_before = OrganismeRecruteurFactory.create_entity(etapes=etapes)
    update_organisme_steps_usecase.organisme_recruteur_repository.save(organisme_before)
    utilisateur_id = uuid4()

    nouvelles_etapes = EtapeRecrutementFactory.to_etape_data_list(etapes)

    organisme = update_organisme_steps_usecase.execute(
        command=UpdateOrganismeStepsCommand(
            utilisateur_id=utilisateur_id,
            organisme_id=organisme_before.entity_id,
            etapes=nouvelles_etapes,
        )
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert events[0].event_name == "OrganismeEtapesMisesAJour"
    assert organisme.etapes is not None
    assert len(organisme.etapes) == len(nouvelles_etapes)
    update_organisme_steps_usecase.audit_log_writer.drain_events.assert_called_once_with(
        utilisateur_id=utilisateur_id, aggregate=organisme
    )
