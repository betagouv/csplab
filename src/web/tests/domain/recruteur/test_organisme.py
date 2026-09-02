from typing import List
from uuid import uuid4

import pytest

from domain.recruteur.entities.etape_recrutement import EtapeRecrutement
from domain.recruteur.entities.organisme_recruteur import OrganismeRecruteur
from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.events.etape_events import (
    EtapeAjoutee,
    EtapeRenommee,
    EtapeReordonnee,
    EtapeSupprimee,
)
from domain.recruteur.events.organisme_recruteur_events import (
    OrganismeEtapesInitialises,
    OrganismeEtapesMisesAJour,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_data import EtapeData
from infrastructure.factories.recruteur.etapes_recrutement_factory import (
    EtapeRecrutementFactory,
)
from infrastructure.factories.recruteur.organisme_factory import (
    OrganismeRecruteurFactory,
)

NB_ETAPES_PAR_DEFAUT = 6
NB_ETAPES_EN_COURS_PAR_DEFAUT = 3
NUMBER_CHANGES = 5


@pytest.fixture(name="etapes")
def etapes_fixture():
    return EtapeRecrutementFactory.create_entity_batch()


@pytest.fixture(name="etapes_data")
def etapes_data_fixture(etapes) -> List[EtapeData]:
    # e3 deleted
    e0, e1, e2, _, e4, e5 = etapes
    return [
        EtapeData(
            etape_uuid=e0.entity_id,
            nom="Candidatures reçues",
            categorie=e0.categorie,
        ),
        EtapeData(
            etape_uuid=None,
            nom="Sourcing",
            categorie=CategorieEtapeRecrutement.EN_COURS,  # added
        ),
        *[
            EtapeData(
                etape_uuid=e.entity_id,
                nom=e.nom,
                categorie=e.categorie,
            )
            for e in [e2, e1, e4, e5]
        ],
    ]


def test_organisme_default_steps(etapes) -> None:
    organisme = OrganismeRecruteur.build(entity_id=uuid4(), etapes=etapes)
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


def test_organisme_update_steps(etapes_data, etapes) -> None:
    organisme = OrganismeRecruteurFactory.create_entity(etapes=etapes)

    organisme.mettre_a_jour_etapes(etapes_data=etapes_data)

    events = organisme.collect_events()
    assert len(events) == NUMBER_CHANGES
    assert any(isinstance(e, OrganismeEtapesMisesAJour) for e in events)
    assert any(isinstance(e, EtapeAjoutee) for e in events)
    assert any(isinstance(e, EtapeSupprimee) for e in events)
    assert any(isinstance(e, EtapeRenommee) for e in events)
    assert any(isinstance(e, EtapeReordonnee) for e in events)


@pytest.mark.parametrize(
    "invalid",
    [
        pytest.param(
            (
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Présélection",
                ),
            ),
            id="no_entry",
        ),
        pytest.param(
            (
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Réception des candidatures",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Entretien",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Avant-dernière EN_COURS au lieu de REFUS",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.ACCEPTE,
                    nom="Recrutement",
                ),
            ),
            id="second_to_last_not_refus",
        ),
        pytest.param(
            (
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Réception des candidatures",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.REFUS,
                    nom="Refus",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.ACCEPTE,
                    nom="Recrutement",
                ),
            ),
            id="no_en_cours",
        ),
        pytest.param(
            (
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Réception des candidatures",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Entretien",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Doublon ENTREE au milieu",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.REFUS,
                    nom="Refus",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.ACCEPTE,
                    nom="Recrutement",
                ),
            ),
            id="middle_contains_non_en_cours",
        ),
        pytest.param(
            (
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Réception des candidatures",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Entretien",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.REFUS,
                    nom="Refus",
                ),
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Étape parasite en fin",
                ),
            ),
            id="last_not_accepte",
        ),
    ],
)
def test_organisme_update_steps_fails(
    invalid: List[EtapeData],
) -> None:
    organisme = OrganismeRecruteurFactory.create_entity(
        etapes=EtapeRecrutementFactory.create_entity_batch()
    )

    with pytest.raises(ConfigurationEtapesInvalide):
        organisme.mettre_a_jour_etapes(etapes_data=tuple(invalid))
