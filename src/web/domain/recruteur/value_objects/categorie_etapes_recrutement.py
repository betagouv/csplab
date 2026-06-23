from enum import Enum


class CategorieEtapeRecrutement(Enum):
    ENTREE = "entree"  # → candidatures reçues
    EN_COURS = "en_cours"  # → preselection, entretien, proposition, refusee
    REFUS = "refus"  # → candidatures refusées
    ACCEPTE = "accepte"  # → candidature acceptée
