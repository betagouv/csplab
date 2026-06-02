from dataclasses import dataclass
from enum import Enum

from domain.recrutement.errors.erreur_recrutement import EtapeRecrutementInvalide


class CategorieEtapeRecrutement(Enum):
    PUBLICATION = "publication"  # → ouvre les candidatures
    RECEPTION = "reception"  # → collecte des dossiers
    EVALUATION = "evaluation"  # → entretien, test, mise en situation...
    SELECTION = "selection"  # → décision finale
    CLOTURE = "cloture"  # → ferme l'offre, notifie les candidats


@dataclass(frozen=True)
class EtapeRecrutement:
    rang: int  # ordre de l'étape dans le processus
    identifiant: str  # identifiant de l'étape
    categorie: CategorieEtapeRecrutement  # catégorie connue du système
    nom: str  # label libre, personnalisé par l'organisme

    def __post_init__(self) -> None:
        erreurs = []
        if not isinstance(self.rang, int) or self.rang <= 0:
            erreurs.append("rang doit être un entier strictement positif")
        if not self.identifiant.strip():
            erreurs.append("identifiant ne peut pas être vide")
        if not isinstance(self.categorie, CategorieEtapeRecrutement):
            erreurs.append("categorie doit être une CategorieEtapeRecrutement valide")
        if not self.nom.strip():
            erreurs.append("nom ne peut pas être vide")
        if erreurs:
            raise EtapeRecrutementInvalide(identifier=self.identifiant, erreurs=erreurs)


@dataclass(frozen=True)
class EtapesRecrutement:
    etapes: tuple[EtapeRecrutement, ...]

    def __post_init__(self) -> None:
        identifiants = [e.identifiant for e in self.etapes]
        doublons = {i for i in identifiants if identifiants.count(i) > 1}
        if doublons:
            raise EtapeRecrutementInvalide(
                identifier="etapes_recrutement",
                erreurs=[f"identifiants en doublon : {sorted(doublons)}"],
            )

    def ordonnees(self) -> tuple[EtapeRecrutement, ...]:
        return tuple(sorted(self.etapes, key=lambda e: e.rang))
