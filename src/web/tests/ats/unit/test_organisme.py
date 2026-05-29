from domain.entities.organisme import Organisme
from domain.events.organisme_events import (
    OrganismeCree,
    ParametresOrganismeConfigures,
    ParametresOrganismeModifies,
)
from domain.value_objects.siret import SIRET
from domain.value_objects.verse import Verse
from tests.factories.organisme_factory import OrganismeFactory


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
            parametres=parent_organisme.parametres,
        )
    )
    assert organisme.nom == "Ecole du Louvre"
    assert organisme.versant == Verse.FPE
    assert organisme.parametres == parent_organisme.parametres
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeCree)
    assert organisme.parent_id == parent_organisme.entity_id
    assert organisme.siret == SIRET("19754687200015")
    assert organisme.localisation == parent_organisme.localisation


def test_organisme_parametres_configures():
    organisme = OrganismeFactory.build()
    organisme.configurer_parametres(
        ParametresOrganismeConfigures(parametres=["Init", "Config"])
    )
    assert organisme.parametres == ["Init", "Config"]
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], ParametresOrganismeConfigures)


def test_organisme_configuration_modifiee():
    organisme = OrganismeFactory.build()
    organisme.modifier_parametres(
        ParametresOrganismeModifies(parametres=["New", "Config"])
    )
    assert organisme.parametres == ["New", "Config"]
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], ParametresOrganismeModifies)
