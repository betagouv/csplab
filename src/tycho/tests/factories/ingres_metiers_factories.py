import uuid
from typing import List, Optional

from polyfactory.factories.pydantic_factory import ModelFactory

from infrastructure.external_gateways.dtos.ingres_metiers_dtos import (
    ActivitesDeLEr,
    Competences,
    Definitions,
    DefinitionSynthetiqueDeLEr,
    DomaineFonctionnelFamille,
    EmploiDeReferenceCSP,
    FonctionPublique,
    IngresMetiersApiResponse,
    IngresMetiersDocument,
    Libelles,
    Specificites,
    Validite,
)


class MetiersLibellesFactory(ModelFactory[Libelles]):
    __model__ = Libelles

    @classmethod
    def libelleCourt(cls) -> str:
        return "Responsable achats"

    @classmethod
    def libelleLong(cls) -> str:
        return "Responsable achats"


class MetiersValiditeFactory(ModelFactory[Validite]):
    __model__ = Validite

    @classmethod
    def status(cls) -> str:
        return "A"

    @classmethod
    def debutValidite(cls) -> str:
        return "2021-09-15T00:00:00Z"

    @classmethod
    def finValidite(cls) -> Optional[str]:
        return None


class FonctionPubliqueFactory(ModelFactory[FonctionPublique]):
    __model__ = FonctionPublique

    @classmethod
    def PFE(cls) -> str:
        return "1"

    @classmethod
    def FPT(cls) -> str:
        return "1"

    @classmethod
    def FPH(cls) -> str:
        return "1"


class DefinitionSynthetiqueDeLErFactory(ModelFactory[DefinitionSynthetiqueDeLEr]):
    __model__ = DefinitionSynthetiqueDeLEr

    @classmethod
    def definition(cls) -> Optional[str]:
        return (
            "Définir, proposer, et mettre en oeuvre la politique achat de sa structure "
            "et les stratégies achat relevant de son périmètre selon les objectifs de "
            "performance assignés. Manager son équipe. Evaluer et suivre la "
            "performance des achats (économique, environnementale, sociale, "
            "accès des PME, innovation...)."
        )


class EmploiDeReferenceCSPFactory(ModelFactory[EmploiDeReferenceCSP]):
    __model__ = EmploiDeReferenceCSP

    @classmethod
    def codeEmploiCSP(cls) -> Optional[str]:
        return "ERACH001"

    @classmethod
    def libelleEmploiCSP(cls) -> Optional[str]:
        return "Responsable achats"


class DomaineFonctionnelFamilleFactory(ModelFactory[DomaineFonctionnelFamille]):
    __model__ = DomaineFonctionnelFamille

    @classmethod
    def codeDomaineFonctionnel(cls) -> str:
        return "ACH"

    @classmethod
    def libelleDomaineFonctionnel(cls) -> str:
        return "Achat"

    @classmethod
    def codeFamille(cls) -> str:
        return "FA0046"

    @classmethod
    def libelleFamille(cls) -> str:
        return "Encadrement"


class DefinitionsFactory(ModelFactory[Definitions]):
    __model__ = Definitions

    libelles = MetiersLibellesFactory
    validite = MetiersValiditeFactory
    fonctionPublique = FonctionPubliqueFactory
    definitionSynthetiqueDeLEr = DefinitionSynthetiqueDeLErFactory
    emploiDeReferenceCSP = EmploiDeReferenceCSPFactory
    domaineFonctionnel_Famille = DomaineFonctionnelFamilleFactory


class ActivitesDeLErFactory(ModelFactory[ActivitesDeLEr]):
    __model__ = ActivitesDeLEr

    @classmethod
    def dateEffet(cls) -> str:
        return "2023-08-01T00:00:00Z"

    @classmethod
    def commentaire(cls) -> str:
        return (
            "Proposer et mettre en oeuvre une organisation de la fonction achat "
            "de sa structure adaptée à ses enjeux et à ses objectifs. "
            "Représenter la fonction achats au sein de diverses instances de "
            "gouvernance. Piloter / Animer le réseau des acteurs de la chaine achat."
        )


class SpecificitesFactory(ModelFactory[Specificites]):
    __model__ = Specificites

    @classmethod
    def specificitesFPE(cls) -> Optional[str]:
        return None

    @classmethod
    def specificitesFPH(cls) -> Optional[str]:
        return None

    @classmethod
    def specificitesFPT(cls) -> Optional[str]:
        return None


class CompetencesFactory(ModelFactory[Competences]):
    __model__ = Competences

    specificites = SpecificitesFactory

    @classmethod
    def activitesDeLEr(cls) -> Optional[List[ActivitesDeLEr]]:
        return ActivitesDeLErFactory.batch(size=2)


class IngresMetiersDocumentFactory(ModelFactory[IngresMetiersDocument]):
    __model__ = IngresMetiersDocument

    definitions = DefinitionsFactory
    competences = CompetencesFactory

    @classmethod
    def identifiant(cls) -> str:
        return f"FPACH{str(uuid.uuid4().int)[:3].zfill(3)}"


class IngresMetiersApiResponseFactory(ModelFactory[IngresMetiersApiResponse]):
    __model__ = IngresMetiersApiResponse

    @classmethod
    def documents(cls) -> List[IngresMetiersDocument]:
        """Generate métiers documents."""
        return IngresMetiersDocumentFactory.batch(size=3)
