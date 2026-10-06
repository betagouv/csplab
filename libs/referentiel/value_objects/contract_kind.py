from referentiel.value_objects._choices import TextChoices


class ContractKind(TextChoices):
    CDD = "CDD", "CDD"
    CDI = "CDI", "CDI"
    CDD_CDI = "CDD ou CDI", "CDD ou CDI"
    CONTRAT_PROJET = "Contrat de projet", "Contrat de projet"
    VACATION = "Payés à l'acte", "Payés à l'acte"
