from datetime import datetime, timezone

from referentiel.entities.organisme import Organisme
from referentiel.events.organisme_events import OrganismeCree, OrganismeModifie
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse

from infrastructure.factories.identite.organisme_factory import OrganismeFactory


def test_organisme_modification_bumps_date_derniere_activite():
    date_creation = datetime(2020, 1, 1, tzinfo=timezone.utc)
    date_derniere_activite = datetime(2020, 1, 2, tzinfo=timezone.utc)
    organisme = OrganismeFactory.create_entity(
        date_creation=date_creation, date_derniere_activite=date_derniere_activite
    )

    organisme.modifier(nom="Commune de Paris", versant=None, gestion_ats=None)

    assert organisme.nom == "Commune de Paris"
    assert organisme.date_creation == date_creation
    assert organisme.date_derniere_activite > date_derniere_activite

    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeModifie)
    assert events[0].nom == "Commune de Paris"
    assert events[0].versant is None
    assert events[0].gestion_ats is None


def test_organisme_creation():
    parent_organisme = OrganismeFactory.create_entity(
        nom=(
            "Etablissement d'enseignement et de recherche"
            "- Ministère chargé de la Culture"
        )
    )
    organisme = Organisme.create(
        nom="Ecole du Louvre",
        versant=Verse.FPE,
        localisation=parent_organisme.localisation,
        siret=SIRET(code="19754687200015"),
        parent_id=parent_organisme.entity_id,
        external_id="ext-123",
    )
    assert organisme.nom == "Ecole du Louvre"
    assert organisme.versant == Verse.FPE
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeCree)
    assert organisme.parent_id == parent_organisme.entity_id
    assert organisme.siret == SIRET(code="19754687200015")
    assert organisme.localisation == parent_organisme.localisation
