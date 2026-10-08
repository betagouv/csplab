from typing import List

import pytest

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


def test_organisme_update_steps_fails() -> None:
    organisme = OrganismeRecruteurFactory.create_entity(
        etapes=EtapeRecrutementFactory.create_entity_batch()
    )
    sans_entree = (
        EtapeData(
            etape_uuid=None,
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Présélection",
        ),
        EtapeData(
            etape_uuid=None,
            categorie=CategorieEtapeRecrutement.EN_COURS,
            nom="Entretien",
        ),
        EtapeData(
            etape_uuid=None,
            categorie=CategorieEtapeRecrutement.REFUS,
            nom="Refus",
        ),
        EtapeData(
            etape_uuid=None,
            categorie=CategorieEtapeRecrutement.ACCEPTE,
            nom="Recrutement",
        ),
    )

    with pytest.raises(ConfigurationEtapesInvalide) as error:
        organisme.mettre_a_jour_etapes(etapes_data=sans_entree)

    assert error.value.raison == "La première étape doit être de catégorie ENTREE"
