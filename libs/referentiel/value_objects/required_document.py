from referentiel.value_objects._choices import TextChoices


class RequiredDocument(TextChoices):
    CV = "CV", "CV"
    LETTRE_MOTIVATION = "Lettre de motivation", "Lettre de motivation"
    PORTFOLIO = "Portfolio", "Portfolio"
