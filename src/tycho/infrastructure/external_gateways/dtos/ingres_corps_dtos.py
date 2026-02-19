"""Pydantic models for Ingres API responses."""

from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict


class Libelles(BaseModel):
    """Labels for a corps."""

    libelleCourt: str
    libelleLong: str
    libelleImpression: str


class Validite(BaseModel):
    """Validity period of a corps."""

    status: str
    debutValidite: str
    finValidite: Optional[str] = None


class ValiditeJuridique(BaseModel):
    """Legal validity of a corps."""

    dateFinJuridique: Optional[str] = None


class CodeLibelle(BaseModel):
    """Generic code/label structure."""

    code: Optional[str] = None
    libelle: Optional[str] = None


class NatureDeCorps(BaseModel):
    """Nature of corps."""

    codeCorps: str
    libelleCorps: str


class Population(BaseModel):
    """Population."""

    codePopulation: str
    libellePopulation: str


class Categorie(BaseModel):
    """Category."""

    codeCategorie: str
    libelleCategorie: str


class Filiere(BaseModel):
    """Career path."""

    codeFiliere: Optional[str] = None
    libelleFiliere: Optional[str] = None


class NiveauDiplome(BaseModel):
    """Diploma level."""

    codeNiveauDiplome: Optional[str] = None
    libelleNiveauDiplome: Optional[str] = None


class NatureFonctionPublique(BaseModel):
    """Public service nature."""

    codeNatureFoncPub: str
    libelleNatureFoncPub: str


class CorpsGenerique(BaseModel):
    """Generic corps."""

    codeCorpsGenerique: Optional[str] = None
    libelleCorpsGenerique: Optional[str] = None


class Caracteristiques(BaseModel):
    """Corps characteristics."""

    natureDeCorps: NatureDeCorps
    population: Population
    categorie: Categorie
    filiere: Optional[Filiere] = None
    nombreGradesActifs: str
    niveauDiplome: Optional[NiveauDiplome] = None
    corpsExtinction: str
    dateMiseEnExtinction: Optional[str] = None
    natureFonctionPublique: NatureFonctionPublique
    corpsGenerique: Optional[CorpsGenerique] = None


class SousCategorie(BaseModel):
    """Sub-category of a corps."""

    dateEffet: str
    codeSousCategorie: str | None = None
    libelleSousCategorie: str | None = None


class MinistereInstitution(BaseModel):
    """Ministry and institution."""

    codeMinistere: str
    libelleMinistere: str


class ModeAccesCorps(BaseModel):
    """Corps access mode."""

    codeModeAccesCorps: str
    libelleModeAccesCorps: str


class DureeStage(BaseModel):
    """Internship duration by access mode."""

    modeAccesCorps: ModeAccesCorps
    dateDebut: str
    dateFin: Optional[str] = None
    dureeStageAnnees: str
    dureeStageMois: str
    commentaire: Optional[str] = None


class TypeTexte(BaseModel):
    """Text type."""

    codeType: str
    libelleType: str


class NatureTexte(BaseModel):
    """Text nature."""

    codeNature: str
    libelleNature: str


class TexteAssocie(BaseModel):
    """Associated text."""

    identifiant: str
    type: TypeTexte
    articles: Optional[Any] = None
    indForcage: Optional[Any] = None
    nature: NatureTexte
    numeroTexte: str | None = None
    dateTexte: str | None = None
    datePublication: str | None = None
    NOR: str | None = None
    legiFrance: Optional[str] = None
    descriptif: str | None = None


class DefinitionsHistoriques(BaseModel):
    """Historical definitions."""

    textesAssocies: List[TexteAssocie]


class Nomenclature(BaseModel):
    """Event nomenclature."""

    referentielNoyau: str
    typeReferentiel: str
    repertoireHRAccess: str
    code: str


class VersionCourante(BaseModel):
    """Current version."""

    version: str
    type: str
    status: str


class SyntheseEvenements(BaseModel):
    """Event synthesis."""

    typeMiseAJourGlobale: str
    statusGlobal: str
    versionCreation: str
    versionCloture: Optional[str] = None
    versionSuppression: Optional[str] = None


class EvenementSurCode(BaseModel):
    """Code event."""

    dateFonctionnelle: Optional[str] = None
    versionNoyau: str
    status: str
    typeMiseAJour: str
    utilisateur: str
    nombreAttributs: str
    horodatageMiseAJour: str


class EvenementsSurCode(BaseModel):
    """Code events."""

    nomenclature: Nomenclature
    versionCourante: VersionCourante
    syntheseDesEvenements: SyntheseEvenements
    evenementsSurCode: List[EvenementSurCode]


class CorpsOuPseudoCorps(BaseModel):
    """Main corps structure."""

    libelles: Libelles
    validite: Validite
    validiteJuridique: ValiditeJuridique
    caracteristiques: Caracteristiques
    sousCategorie: Optional[List[SousCategorie]] = None
    ministereEtInstitutionDeLaRepublique: List[MinistereInstitution]
    specialite: Optional[Any] = None
    corpsAnterieurs: Optional[Any] = None
    corpsSuccesseurs: Optional[Any] = None
    dureeDeStageParModeAccesAuCorps: Optional[List[DureeStage]] = None


class IngresCorpsDocument(BaseModel):
    """Complete Ingres corps document."""

    model_config = ConfigDict(extra="ignore")

    identifiant: str
    corpsOuPseudoCorps: CorpsOuPseudoCorps
    evenementsSurCode: EvenementsSurCode
    definitionsHistoriques: Optional[DefinitionsHistoriques] = None


class IngresCorpsApiResponse(BaseModel):
    """Complete Ingres API response for corps."""

    documents: List[IngresCorpsDocument]

    @classmethod
    def from_list(cls, data: List[dict]) -> "IngresCorpsApiResponse":
        """Create instance from a list of documents."""
        documents = [IngresCorpsDocument(**doc) for doc in data]
        return cls(documents=documents)
