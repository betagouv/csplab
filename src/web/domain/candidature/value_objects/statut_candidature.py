from enum import Enum


class StatutCandidature(Enum):
    SOUMISE      = "soumise"        # état initial à la soumission
    EN_COURS     = "en_cours"       # en cours d'instruction par le RH
    REFUSEE      = "refusee"        # candidature refusée
    SELECTIONNEE = "selectionnee"   # candidature retenue
    INCOMPLETE    = "incomplete"    # candidature incomplète, en attente de compléments d'information
