from referentiel.value_objects._choices import TextChoices


class Management(TextChoices):
    SANS = "Sans management", "Sans management"
    AVEC = "Avec management", "Avec management"


class WorkingPlace(TextChoices):
    NON_DEFINI = "Non défini", "Non défini"
    SUR_SITE = "Sur site", "Sur site"
    TELETRAVAIL = "Télétravail", "Télétravail"


class OpenToMilitary(TextChoices):
    NON = "Non", "Non"
    OUI = "Oui", "Oui"


class WorkingTime(TextChoices):
    NON_DEFINI = "Non défini", "Non défini"
    TEMPS_PLEIN = "Temps plein", "Temps plein"
    TEMPS_PARTIEL = "Temps incomplet", "Temps incomplet"


class JobVacancy(TextChoices):
    OUI = "Poste vacant", "Poste vacant"
    NON = "Poste susceptible d'être vacant", "Poste susceptible d'être vacant"
