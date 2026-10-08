from collections.abc import Sequence

from domain.recruteur.errors.organisme_recruteur_errors import (
    ConfigurationEtapesInvalide,
)
from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)
from domain.recruteur.value_objects.etape_data import EtapeData


def valider_sequence_etapes(etapes: Sequence[EtapeData]) -> None:
    categories = [e.categorie for e in etapes]
    if not categories or categories[0] != CategorieEtapeRecrutement.ENTREE:
        raise ConfigurationEtapesInvalide(
            "La première étape doit être de catégorie ENTREE"
        )
    elif categories[-1] != CategorieEtapeRecrutement.ACCEPTE:
        raise ConfigurationEtapesInvalide(
            "La dernière étape doit être de catégorie ACCEPTE"
        )
    elif categories[-2] != CategorieEtapeRecrutement.REFUS:
        raise ConfigurationEtapesInvalide(
            "L'avant-dernière étape doit être de catégorie REFUS"
        )

    milieu = categories[1:-2]
    if not milieu:
        raise ConfigurationEtapesInvalide("Il doit y avoir au moins une étape EN_COURS")
    if any(c != CategorieEtapeRecrutement.EN_COURS for c in milieu):
        raise ConfigurationEtapesInvalide(
            "Seules les étapes EN_COURS peuvent être placées entre ENTREE et REFUS"
        )

    couples = {(e.nom, e.categorie) for e in etapes}
    if len(couples) != len(etapes):
        raise ConfigurationEtapesInvalide(
            "Chaque couple (nom, catégorie) doit être unique"
        )
