from enum import Enum

from domain.recruteur.value_objects.etape_action import EtapeAction


class CategorieEtapeRecrutement(Enum):
    ENTREE = "entree"  # → candidatures reçues
    EN_COURS = "en_cours"  # → preselection, entretien, proposition, refusee
    REFUS = "refus"  # → candidatures refusées
    ACCEPTE = "accepte"  # → candidature acceptée

    @property
    def actions(self) -> list[EtapeAction]:
        return ACTIONS_BY_CATEGORIE[self]


ACTIONS_BY_CATEGORIE: dict[CategorieEtapeRecrutement, list[EtapeAction]] = {
    CategorieEtapeRecrutement.ENTREE: [EtapeAction.INSERT_ETAPE_AFTER],
    CategorieEtapeRecrutement.EN_COURS: list(EtapeAction),
    CategorieEtapeRecrutement.REFUS: [EtapeAction.INSERT_ETAPE_BEFORE],
    CategorieEtapeRecrutement.ACCEPTE: [],
}
