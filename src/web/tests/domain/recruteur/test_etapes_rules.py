from uuid import uuid4

import pytest

from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.etapes_rules import valider_sequence_etapes
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_data import EtapeData


def test_accepts_well_formed_sequence() -> None:
    valider_sequence_etapes(
        (
            EtapeData(
                etape_uuid=None,
                categorie=CategorieEtapeRecrutement.ENTREE,
                nom="Réception des candidatures",
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
    )


@pytest.mark.parametrize(
    ("invalid", "raison"),
    [
        pytest.param((), "La première étape doit être de catégorie ENTREE", id="empty"),
        pytest.param(
            (
                EtapeData(
                    etape_uuid=uuid4(),
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Présélection",
                ),
            ),
            "La première étape doit être de catégorie ENTREE",
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
            "L'avant-dernière étape doit être de catégorie REFUS",
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
            "Il doit y avoir au moins une étape EN_COURS",
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
            "Seules les étapes EN_COURS peuvent être placées entre ENTREE et REFUS",
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
            "La dernière étape doit être de catégorie ACCEPTE",
            id="last_not_accepte",
        ),
        pytest.param(
            (
                EtapeData(
                    etape_uuid=None,
                    categorie=CategorieEtapeRecrutement.ENTREE,
                    nom="Réception des candidatures",
                ),
                EtapeData(
                    etape_uuid=None,
                    categorie=CategorieEtapeRecrutement.EN_COURS,
                    nom="Entretien",
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
            ),
            "Chaque couple (nom, catégorie) doit être unique",
            id="duplicate_nom_categorie",
        ),
    ],
)
def test_rejects_malformed_sequence(invalid: tuple[EtapeData, ...], raison) -> None:
    with pytest.raises(ConfigurationEtapesInvalide) as error:
        valider_sequence_etapes(invalid)

    assert error.value.raison == raison
