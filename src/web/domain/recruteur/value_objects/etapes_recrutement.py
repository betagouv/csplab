from dataclasses import dataclass
from enum import Enum

from domain.recruteur.errors.erreur_recrutement import EtapeInvalide


class CategorieEtapeRecrutement(Enum):
    INITIALE = "initiale"  # → ouvre les candidatures
    EN_COURS = "en_cours"  # → entretien, test, mise en situation...
    TERMINALE = "terminale"  # → ferme l'offre, notifie les candidats


@dataclass(frozen=True)
class EtapeRecrutement:
    identifiant: str  # identifiant de l'étape
    categorie: CategorieEtapeRecrutement  # catégorie connue du système
    nom: str  # label libre, personnalisé par l'organisme

    def __post_init__(self) -> None:
        erreurs = []
        if not self.identifiant.strip():
            erreurs.append("identifiant ne peut pas être vide")
        if not isinstance(self.categorie, CategorieEtapeRecrutement):
            erreurs.append("categorie doit être une CategorieEtapeRecrutement valide")
        if not self.nom.strip():
            erreurs.append("nom ne peut pas être vide")
        if erreurs:
            raise EtapeInvalide(identifier=self.identifiant, erreurs=erreurs)


@dataclass(frozen=True)
class EtapesRecrutement:
    etapes: tuple[EtapeRecrutement, ...]  # l'ordre du tuple définit l'ordre des étapes

    def __post_init__(self) -> None:
        identifiants = [e.identifiant for e in self.etapes]
        doublons = {i for i in identifiants if identifiants.count(i) > 1}
        if doublons:
            raise EtapeInvalide(
                identifier="etapes_recrutement",
                erreurs=[f"identifiants en doublon : {sorted(doublons)}"],
            )
