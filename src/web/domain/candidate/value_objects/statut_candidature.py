from enum import Enum


class StatutCandidature(Enum):
    INITIAL = "initial"  # état par défaut, avant soumission
    SOUMISE = "soumise"  # état initial à la soumission
    RETIREE = "retiree"  # candidature retirée
