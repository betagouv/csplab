from django.db.models import TextChoices


class ContractType(TextChoices):
    TITULAIRE_CONTRACTUEL = (
        "TITULAIRE_CONTRACTUEL",
        "Emploi ouvert aux titulaires et aux contractuels",
    )
    CONTRACTUELS = "CONTRACTUELS", "Emploi ouvert uniquement aux contractuels"
    TERRITORIAL = (
        "TERRITORIAL",
        "Emploi réservé aux fonctionnaires et lauréats d'un concours territorial",
    )


class ContractKind(TextChoices):
    CDD = "CDD", "CDD"
    CDI = "CDI", "CDI"
    PERMANENT = "Permanent", "Permanent"
    VACATION = "Vacation", "Vacation"
