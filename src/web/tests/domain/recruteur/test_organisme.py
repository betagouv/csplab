from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.events.organisme_events import OrganismeEtapesInitialises
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from tests.factories.recruteur.organisme_factory import OrganismeRecruteurFactory

NB_ETAPES_PAR_DEFAUT = 6
NB_ETAPES_EN_COURS_PAR_DEFAUT = 4


def test_organisme_default_steps() -> None:
    organisme = OrganismeRecruteurFactory.create_entity()
    organisme.initialiser_etapes()
    events = organisme.collect_events()
    assert len(events) == 1
    assert isinstance(events[0], OrganismeEtapesInitialises)
    steps = organisme.etapes
    assert steps is not None
    assert len(steps) == NB_ETAPES_PAR_DEFAUT
    categories = [e.categorie for e in steps]
    assert categories.count(CategorieEtapeRecrutement.ENTREE) == 1
    assert (
        categories.count(CategorieEtapeRecrutement.EN_COURS)
        == NB_ETAPES_EN_COURS_PAR_DEFAUT
    )
    assert categories.count(CategorieEtapeRecrutement.TERMINALE) == 1
    first_step = EtapeRecrutement.create(
        categorie=CategorieEtapeRecrutement.ENTREE,
        nom="Réception des candidatures",
    )
    assert steps[0].nom == first_step.nom
