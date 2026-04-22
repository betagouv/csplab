from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict


class Libelles(BaseModel):
    libelleCourt: str
    libelleLong: str


class Validite(BaseModel):
    status: str
    debutValidite: str
    finValidite: Optional[str] = None


class FonctionPublique(BaseModel):
    PFE: str
    FPT: str
    FPH: str


class DefinitionSynthetiqueDeLEr(BaseModel):
    definition: Optional[str] = None


class EmploiDeReferenceCSP(BaseModel):
    codeEmploiCSP: Optional[str] = None
    libelleEmploiCSP: Optional[str] = None


class DomaineFonctionnelFamille(BaseModel):
    codeDomaineFonctionnel: str
    libelleDomaineFonctionnel: str
    codeFamille: str
    libelleFamille: str


class Definitions(BaseModel):
    libelles: Libelles
    validite: Validite
    fonctionPublique: FonctionPublique
    definitionSynthetiqueDeLEr: DefinitionSynthetiqueDeLEr
    emploiDeReferenceCSP: EmploiDeReferenceCSP
    domaineFonctionnel_Famille: DomaineFonctionnelFamille


class ActivitesDeLEr(BaseModel):
    dateEffet: str
    commentaire: str


class ConditionsParticulieresDExerciceDAcces(BaseModel):
    dateEffet: str
    commentaire: str


class Specificites(BaseModel):
    specificitesFPE: Optional[Any] = None
    specificitesFPH: Optional[Any] = None
    specificitesFPT: Optional[Any] = None


class Competences(BaseModel):
    activitesDeLEr: Optional[List[ActivitesDeLEr]] = None
    conditionsParticulieresDExerciceDAcces: Optional[
        List[ConditionsParticulieresDExerciceDAcces]
    ] = None
    specificites: Specificites


class IngresMetiersDocument(BaseModel):
    model_config = ConfigDict(extra="ignore")

    identifiant: str
    definitions: Definitions
    competences: Competences


class IngresMetiersApiResponse(BaseModel):
    documents: List[IngresMetiersDocument]

    @classmethod
    def from_list(cls, data: List[dict]) -> "IngresMetiersApiResponse":
        documents = [IngresMetiersDocument(**doc) for doc in data]
        return cls(documents=documents)
