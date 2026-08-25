from uuid import uuid4

from referentiel.entities.organisme import Organisme
from referentiel.events.organisme_events import OrganismeCree, OrganismeRemplace
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse


def test_organisme_create_emits_organisme_cree():
    organisme = Organisme.create(
        nom="Commune de Paris",
        versant=Verse.FPT,
        localisation=None,
        siret=SIRET(code="19754687200015"),
        parent_id=None,
        external_id="ext-123",
        referentiel="FINESS",
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeCree)
    assert organisme.nom == "Commune de Paris"
    assert organisme.external_id == "ext-123"
    assert organisme.referentiel == "FINESS"


def test_organisme_remplacer_emits_organisme_remplace():
    organisme = Organisme.build(
        entity_id=uuid4(),
        nom="Ancien nom",
        versant=Verse.FPT,
        localisation=None,
        siret=SIRET(code="19754687200015"),
        parent_id=None,
        external_id="ext-123",
        referentiel="FINESS",
    )

    organisme.remplacer(
        nom="Nouveau nom",
        versant=Verse.FPE,
        localisation=None,
        siret=SIRET(code="19754687200015"),
        parent_id=None,
        external_id="ext-123",
        referentiel="FINESS",
    )

    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeRemplace)
    assert organisme.nom == "Nouveau nom"
    assert organisme.versant == Verse.FPE
