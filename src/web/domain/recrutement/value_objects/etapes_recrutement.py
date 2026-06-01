from dataclasses import dataclass
from enum import Enum

from domain.recrutement.errors.erreur_recrutement import RecrutementInvalide


class CategorieEtapeRecrutement(Enum):
    PUBLICATION = "publication"  # → ouvre les candidatures
    RECEPTION = "reception"  # → collecte des dossiers
    EVALUATION = "evaluation"  # → entretien, test, mise en situation...
    SELECTION = "selection"  # → décision finale
    CLOTURE = "cloture"  # → ferme l'offre, notifie les candidats


@dataclass(frozen=True)
class EtapeRecrutement:
    rang: int  # ordre de l'étape dans le processus
    identifiant: str  # clé unique pour référencer l'étape
    categorie: CategorieEtapeRecrutement  # catégorie connue du système
    nom: str  # label libre, personnalisé par l'organisme

    def __post_init__(self) -> None:
        erreurs = []
        if not isinstance(self.rang, int) or self.rang <= 0:
            erreurs.append("rang doit être un entier strictement positif")
        if not self.identifiant.strip():
            erreurs.append("identifiant ne peut pas être vide")
        if not self.nom.strip():
            erreurs.append("nom ne peut pas être vide")
        if erreurs:
            raise RecrutementInvalide(identifier=self.identifiant, erreurs=erreurs)


@dataclass(frozen=True)
class EtapesRecrutement:
    etapes: tuple[EtapeRecrutement, ...]

    def ordonnees(self) -> tuple[EtapeRecrutement, ...]:
        return tuple(sorted(self.etapes, key=lambda e: e.rang))
