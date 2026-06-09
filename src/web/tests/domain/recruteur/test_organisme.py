from domain.recruteur.events.organisme_events import (
    OrganismeParametresInitialises,
    OrganismeParametresModifies,
)
from tests.factories.recruteur.organisme_factory import OrganismeFactory


def test_organisme_parametres_initialises():
    organisme = OrganismeFactory.build()
    organisme.initialiser_parametres(
        OrganismeParametresInitialises(parametres=organisme.parametres)
    )
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeParametresInitialises)


def test_organisme_configuration_modifiee():
    organisme = OrganismeFactory.build()
    organisme.modifier_parametres(
        OrganismeParametresModifies(parametres=organisme.parametres)
    )
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeParametresModifies)
