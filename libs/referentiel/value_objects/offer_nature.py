from referentiel.value_objects._choices import TextChoices


class OfferNature(TextChoices):
    TITULAIRE_CONTRACTUEL = (
        "TITULAIRE_CONTRACTUEL",
        "Ouvert aux fonctionnaires et aux contractuels",
    )
    CONTRACTUEL = "CONTRACTUEL", "Ouvert uniquement aux contractuels"
    TERRITORIAL = (
        "TERRITORIAL",
        "Ouvert aux fonctionnaires et lauréats d'un concours territorial",
    )
