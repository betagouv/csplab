from dataclasses import dataclass

from referentiel.value_objects._choices import TextChoices


class RequiredDocument(TextChoices):
    CV = "CV", "CV"
    LETTRE_MOTIVATION = "Lettre de motivation", "Lettre de motivation"
    PORTFOLIO = "Portfolio", "Portfolio"


@dataclass(frozen=True)
class TalentsoftRequiredDocuments:
    client_code: str
    label: str
    documents: tuple[RequiredDocument, ...]


TALENTSOFT_REQUIRED_DOCUMENTS: tuple[TalentsoftRequiredDocuments, ...] = (
    TalentsoftRequiredDocuments(
        client_code="Doc_CV",
        label="L'envoi du CV est obligatoire",
        documents=(RequiredDocument.CV,),
    ),
    TalentsoftRequiredDocuments(
        client_code="Doc_CV_LM",
        label="L'envoi du CV et d'une lettre de motivation est obligatoire",
        documents=(RequiredDocument.CV, RequiredDocument.LETTRE_MOTIVATION),
    ),
    TalentsoftRequiredDocuments(
        client_code="Doc_CV_PF",
        label="L'envoi du CV et d'un portfolio est obligatoire",
        documents=(RequiredDocument.CV, RequiredDocument.PORTFOLIO),
    ),
    TalentsoftRequiredDocuments(
        client_code="Doc_CV_LM_PF",
        label=(
            "L'envoi du CV, d'une lettre de motivation et d'un portfolio "
            "est obligatoire"
        ),
        documents=(
            RequiredDocument.CV,
            RequiredDocument.LETTRE_MOTIVATION,
            RequiredDocument.PORTFOLIO,
        ),
    ),
)
