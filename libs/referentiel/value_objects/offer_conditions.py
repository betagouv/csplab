from enum import Enum


class Management(Enum):
    SANS = "Sans management"
    AVEC = "Avec management"

    def __str__(self):
        return self.value


class WorkingPlace(Enum):
    NON_DEFINI = "Non défini"
    SUR_SITE = "Sur site"
    TELETRAVAIL = "Télétravail"

    def __str__(self):
        return self.value


class OpenToMilitary(Enum):
    NON = "Non"
    OUI = "Oui"

    def __str__(self):
        return self.value


class WorkingTime(Enum):
    NON_DEFINI = "Non défini"
    TEMPS_PLEIN = "Temps plein"
    TEMPS_PARTIEL = "Temps incomplet"

    def __str__(self):
        return self.value


class JobVacancy(Enum):
    OUI = "Poste vacant"
    NON = "Poste susceptible d'être vacant"

    def __str__(self):
        return self.value
