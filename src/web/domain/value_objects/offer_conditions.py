from enum import Enum


class Management(Enum):
    SANS = "Sans management"
    AVEC = "Avec management"

    def __str__(self):
        return self.value


class WorkingPlace(Enum):
    NONDEFINI = "Non défini"
    SURSITE = "Sur site"
    TELETRAVAIL = "Télétravail"

    def __str__(self):
        return self.value


class OpenToMilitary(Enum):
    NON = "Non"
    OUI = "Oui"

    def __str__(self):
        return self.value


class WorkingTime(Enum):
    NONDEFINI = "Non défini"
    TEMPSPLEIN = "Temps plein"
    TEMPSPARTIEL = "Temps partiel"

    def __str__(self):
        return self.value


class JobVacancy(Enum):
    OUI = "Poste vacant"
    NON = "Poste susceptible d'être vacant"

    def __str__(self):
        return self.value
