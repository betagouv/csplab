import pytest

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.errors.erreur_recrutement import ConfigurationEtapesInvalide
from domain.recruteur.events.organisme_events import (
    OrganismeEtapesInitialises,
    OrganismeEtapesMisesAJour,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.organisme_factory import (
    OrganismeRecruteurFactory,
)

NB_ETAPES_PAR_DEFAUT = 6
NB_ETAPES_EN_COURS_PAR_DEFAUT = 3


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
    assert categories.count(CategorieEtapeRecrutement.REFUS) == 1
    assert categories.count(CategorieEtapeRecrutement.ACCEPTE) == 1
    first_step = EtapeRecrutement.create(
        categorie=CategorieEtapeRecrutement.ENTREE,
        nom="Réception des candidatures",
    )
    assert steps[0].nom == first_step.nom


def test_organisme_update_steps() -> None:
    organisme = OrganismeRecruteurFactory.create_entity(
        etapes=EtapeRecrutementFactory.create_entities()
    )
    nouvelles_etapes = (
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.ENTREE,
            nom="Candidatures reçues",
        ),
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Entretien RH",
        ),
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.REFUS,
            nom="Refus",
        ),
        EtapeRecrutement.create(
            categorie=CategorieEtapeRecrutement.ACCEPTE,
            nom="Recrutement",
        ),
    )

    organisme.mettre_a_jour_etapes(etapes=nouvelles_etapes)

    events = organisme.collect_events()
    assert len(events) == 1
    event = events[0]
    assert isinstance(event, OrganismeEtapesMisesAJour)
    assert event.etapes == nouvelles_etapes
    assert organisme.etapes == nouvelles_etapes


@pytest.mark.parametrize(
    "etapes_invalides",
    [
        pytest.param(
            (
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Présélection",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.REFUS,
                    nom="Refus",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.ACCEPTE,
                    nom="Recrutement",
                ),
            ),
            id="no_entry",
        ),
        pytest.param(
            (
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Réception des candidatures",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Entretien",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Avant-dernière EN_COURS au lieu de REFUS",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.ACCEPTE,
                    nom="Recrutement",
                ),
            ),
            id="second_to_last_not_refus",
        ),
        pytest.param(
            (
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Réception des candidatures",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.REFUS,
                    nom="Refus",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.ACCEPTE,
                    nom="Recrutement",
                ),
            ),
            id="no_en_cours",
        ),
        pytest.param(
            (
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Réception des candidatures",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Entretien",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Doublon ENTREE au milieu",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.REFUS,
                    nom="Refus",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.ACCEPTE,
                    nom="Recrutement",
                ),
            ),
            id="middle_contains_non_en_cours",
        ),
        pytest.param(
            (
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Réception des candidatures",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Entretien",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.REFUS,
                    nom="Refus",
                ),
                EtapeRecrutementFactory.create_entity(
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Étape parasite en fin",
                ),
            ),
            id="last_not_accepte",
        ),
    ],
)
def test_organisme_update_steps_fails(
    etapes_invalides: tuple[EtapeRecrutement, ...],
) -> None:
    organisme = OrganismeRecruteurFactory.create_entity(
        etapes=EtapeRecrutementFactory.create_entities()
    )

    with pytest.raises(ConfigurationEtapesInvalide):
        organisme.mettre_a_jour_etapes(etapes=etapes_invalides)
