from enum import Enum

from domain.recruteur.value_objects.categorie_etapes_recrutement import (
    CategorieEtapeRecrutement,
)


class EtapeParDefaut(Enum):
    RECEPTION = (CategorieEtapeRecrutement.ENTREE, "Réception des candidatures")
    PRESELECTION = (CategorieEtapeRecrutement.EN_COURS, "Présélection")
    ENTRETIEN = (CategorieEtapeRecrutement.EN_COURS, "Entretien")
    PROPOSITION = (CategorieEtapeRecrutement.EN_COURS, "Proposition")
    REFUS = (CategorieEtapeRecrutement.REFUS, "Refus")
    RECRUTEMENT = (CategorieEtapeRecrutement.ACCEPTE, "Recrutement")

    def __init__(self, categorie: CategorieEtapeRecrutement, nom: str) -> None:
        self.categorie = categorie
        self.nom = nom
