from referentiel.value_objects._choices import TextChoices


class ContractType(TextChoices):
    TITULAIRE_CONTRACTUEL = (
        "TITULAIRE_CONTRACTUEL",
        "Ouvert aux fonctionnaires et aux contractuels",
    )
    CONTRACTUEL = "CONTRACTUEL", "Ouvert uniquement aux contractuels"
    TERRITORIAL = (
        "TERRITORIAL",
        "Ouvert aux fonctionnaires et lauréats d'un concours territorial",
    )


class ContractKind(TextChoices):
    CDD = "CDD", "CDD"
    CDI = "CDI", "CDI"
    CDD_CDI = "CDD ou CDI", "CDD ou CDI"
    CONTRAT_PROJET = "Contrat de projet", "Contrat de projet"
    VACATION = "Payés à l'acte", "Payés à l'acte"
