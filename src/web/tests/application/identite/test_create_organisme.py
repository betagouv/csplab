from referentiel.value_objects.verse import Verse

from application.identite.usecases.create_organisme import CreateOrganismeCommand
from domain.identite.events.organisme_events import OrganismeCree


def test_create_organisme_success(create_organisme_usecase):
    command = CreateOrganismeCommand(
        nom="Commune de Paris",
        versant=Verse.FPT,
        localisation=None,
        siret=None,
        parent_id=None,
    )

    organisme = create_organisme_usecase.execute(input_data=command)

    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeCree)
    assert organisme.nom == "Commune de Paris"
    assert organisme.versant == Verse.FPT
