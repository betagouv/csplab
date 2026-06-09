from referentiel.value_objects.verse import Verse

from domain.identite.entities.organisme import Organisme
from domain.identite.events.organisme_events import (
    OrganismeCree,
)
from domain.identite.value_objects.siret import SIRET
from tests.factories.identite.organisme_factory import OrganismeFactory


def test_organisme_creation():
    parent_organisme = OrganismeFactory.build(
        nom=(
            "Etablissement d'enseignement et de recherche"
            "- Ministère chargé de la Culture"
        )
    )
    organisme = Organisme.create(
        OrganismeCree(
            nom="Ecole du Louvre",
            versant=Verse.FPE,
            localisation=parent_organisme.localisation,
            siret=SIRET("19754687200015"),
            parent_id=parent_organisme.entity_id,
        )
    )
    assert organisme.nom == "Ecole du Louvre"
    assert organisme.versant == Verse.FPE
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeCree)
    assert organisme.parent_id == parent_organisme.entity_id
    assert organisme.siret == SIRET("19754687200015")
    assert organisme.localisation == parent_organisme.localisation
