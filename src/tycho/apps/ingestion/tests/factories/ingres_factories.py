"""Polyfactory factories for generating test data for Ingres API responses."""

import uuid
from typing import List

from polyfactory.factories.pydantic_factory import ModelFactory

from apps.ingestion.infrastructure.adapters.external.dtos.ingres_corps_dtos import (
    Caracteristiques,
    Categorie,
    CorpsGenerique,
    CorpsOuPseudoCorps,
    DefinitionsHistoriques,
    DureeStage,
    EvenementsSurCode,
    EvenementSurCode,
    Filiere,
    IngresCorpsApiResponse,
    IngresCorpsDocument,
    Libelles,
    MinistereInstitution,
    ModeAccesCorps,
    NatureDeCorps,
    NatureFonctionPublique,
    NatureTexte,
    NiveauDiplome,
    Nomenclature,
    Population,
    SousCategorie,
    SyntheseEvenements,
    TexteAssocie,
    TypeTexte,
    Validite,
    ValiditeJuridique,
    VersionCourante,
)


class LibellesFactory(ModelFactory[Libelles]):
    """Factory for Libelles."""

    __model__ = Libelles

    @classmethod
    def libelleCourt(cls) -> str:
        """Generate short label."""
        return "PROF LYCE PROF AGRI"

    @classmethod
    def libelleLong(cls) -> str:
        """Generate long label."""
        return "Professeurs de lycée professionnel agricole"

    @classmethod
    def libelleImpression(cls) -> str:
        """Generate print label."""
        return "Professeurs de lycée professionnel agricole"


class ValiditeFactory(ModelFactory[Validite]):
    """Factory for Validite."""

    __model__ = Validite

    @classmethod
    def status(cls) -> str:
        """Generate status."""
        return "A"

    @classmethod
    def debutValidite(cls) -> str:
        """Generate validity start date."""
        return "1989-09-01T00:00:00Z"


class ValiditeJuridiqueFactory(ModelFactory[ValiditeJuridique]):
    """Factory for ValiditeJuridique."""

    __model__ = ValiditeJuridique


class NatureDeCorpsFactory(ModelFactory[NatureDeCorps]):
    """Factory for NatureDeCorps."""

    __model__ = NatureDeCorps

    @classmethod
    def codeCorps(cls) -> str:
        """Generate corps code."""
        return "3"

    @classmethod
    def libelleCorps(cls) -> str:
        """Generate corps label."""
        return "Spécifique"


class PopulationFactory(ModelFactory[Population]):
    """Factory for Population."""

    __model__ = Population

    @classmethod
    def codePopulation(cls) -> str:
        """Generate population code."""
        return "1"

    @classmethod
    def libellePopulation(cls) -> str:
        """Generate population label."""
        return "Fonctionnaire"


class CategorieFactory(ModelFactory[Categorie]):
    """Factory for Categorie."""

    __model__ = Categorie

    @classmethod
    def codeCategorie(cls) -> str:
        """Generate category code."""
        return "1"

    @classmethod
    def libelleCategorie(cls) -> str:
        """Generate category label."""
        return "catégorie A"


class FiliereFactory(ModelFactory[Filiere]):
    """Factory for Filiere."""

    __model__ = Filiere


class NiveauDiplomeFactory(ModelFactory[NiveauDiplome]):
    """Factory for NiveauDiplome."""

    __model__ = NiveauDiplome

    @classmethod
    def codeNiveauDiplome(cls) -> str:
        """Generate diploma level code."""
        return "G"

    @classmethod
    def libelleNiveauDiplome(cls) -> str:
        """Generate diploma level label."""
        return "Niveau 7 Master/diplômes équivalents"


class NatureFonctionPubliqueFactory(ModelFactory[NatureFonctionPublique]):
    """Factory for NatureFonctionPublique."""

    __model__ = NatureFonctionPublique

    @classmethod
    def codeNatureFoncPub(cls) -> str:
        """Generate public function nature code."""
        return "1"

    @classmethod
    def libelleNatureFoncPub(cls) -> str:
        """Generate public function nature label."""
        return "FPE"


class CorpsGeneriqueFactory(ModelFactory[CorpsGenerique]):
    """Factory for CorpsGenerique."""

    __model__ = CorpsGenerique

    @classmethod
    def codeCorpsGenerique(cls) -> str:
        """Generate generic corps code."""
        return "00016"

    @classmethod
    def libelleCorpsGenerique(cls) -> str:
        """Generate generic corps label."""
        return "CG PROF UNIV ET ASSI"


class CaracteristiquesFactory(ModelFactory[Caracteristiques]):
    """Factory for Caracteristiques."""

    __model__ = Caracteristiques

    natureDeCorps = NatureDeCorpsFactory
    population = PopulationFactory
    categorie = CategorieFactory
    filiere = FiliereFactory
    niveauDiplome = NiveauDiplomeFactory
    natureFonctionPublique = NatureFonctionPubliqueFactory
    corpsGenerique = CorpsGeneriqueFactory

    @classmethod
    def nombreGradesActifs(cls) -> str:
        """Generate number of active grades."""
        return "0"

    @classmethod
    def corpsExtinction(cls) -> str:
        """Generate corps extinction status."""
        return "0"


class SousCategorieFactory(ModelFactory[SousCategorie]):
    """Factory for SousCategorie."""

    __model__ = SousCategorie

    @classmethod
    def dateEffet(cls) -> str:
        """Generate effective date."""
        return "1989-10-01T00:00:00Z"

    @classmethod
    def codeSousCategorie(cls) -> str:
        """Generate subcategory code."""
        return "1"

    @classmethod
    def libelleSousCategorie(cls) -> str:
        """Generate subcategory label."""
        return "A+"


class MinistereInstitutionFactory(ModelFactory[MinistereInstitution]):
    """Factory for MinistereInstitution."""

    __model__ = MinistereInstitution

    @classmethod
    def codeMinistere(cls) -> str:
        """Generate ministry code."""
        return "MI130"

    @classmethod
    def libelleMinistere(cls) -> str:
        """Generate ministry label."""
        return "MAA"


class ModeAccesCorpsFactory(ModelFactory[ModeAccesCorps]):
    """Factory for ModeAccesCorps."""

    __model__ = ModeAccesCorps

    @classmethod
    def codeModeAccesCorps(cls) -> str:
        """Generate corps access mode code."""
        return "AC101"

    @classmethod
    def libelleModeAccesCorps(cls) -> str:
        """Generate corps access mode label."""
        return "Concours externe"


class DureeStageFactory(ModelFactory[DureeStage]):
    """Factory for DureeStage."""

    __model__ = DureeStage

    modeAccesCorps = ModeAccesCorpsFactory

    @classmethod
    def dateDebut(cls) -> str:
        """Generate start date."""
        return "1989-09-01T00:00:00Z"

    @classmethod
    def dureeStageAnnees(cls) -> str:
        """Generate internship duration in years."""
        return "1"

    @classmethod
    def dureeStageMois(cls) -> str:
        """Generate internship duration in months."""
        return "0"


class TypeTexteFactory(ModelFactory[TypeTexte]):
    """Factory for TypeTexte."""

    __model__ = TypeTexte

    @classmethod
    def codeType(cls) -> str:
        """Generate text type code."""
        return "01"

    @classmethod
    def libelleType(cls) -> str:
        """Generate text type label."""
        return "Décret"


class NatureTexteFactory(ModelFactory[NatureTexte]):
    """Factory for NatureTexte."""

    __model__ = NatureTexte

    @classmethod
    def codeNature(cls) -> str:
        """Generate text nature code."""
        return "1"

    @classmethod
    def libelleNature(cls) -> str:
        """Generate text nature label."""
        return "Texte d'origine"


class TexteAssocieFactory(ModelFactory[TexteAssocie]):
    """Factory for TexteAssocie."""

    __model__ = TexteAssocie

    type = TypeTexteFactory
    nature = NatureTexteFactory

    @classmethod
    def identifiant(cls) -> str:
        """Generate identifier."""
        return "00000000071"

    @classmethod
    def numeroTexte(cls) -> str:
        """Generate text number."""
        return "90-90"

    @classmethod
    def dateTexte(cls) -> str:
        """Generate text date."""
        return "1990-01-24T00:00:00Z"

    @classmethod
    def datePublication(cls) -> str:
        """Generate publication date."""
        return "1990-01-24T00:00:00Z"

    @classmethod
    def NOR(cls) -> str:
        """Generate NOR number."""
        return "AGRA8902379D"

    @classmethod
    def legiFrance(cls) -> str:
        """Generate LegiFrance reference."""
        return "JORFTEXT000000707201"

    @classmethod
    def descriptif(cls) -> str:
        """Generate description."""
        return (
            "Décret n° 90-90 du 24 janvier 1990 relatif au statut particulier "
            "des professeurs de lycée professionnel agricole"
        )


class DefinitionsHistoriquesFactory(ModelFactory[DefinitionsHistoriques]):
    """Factory for DefinitionsHistoriques."""

    __model__ = DefinitionsHistoriques

    @classmethod
    def textesAssocies(cls) -> List[TexteAssocie]:
        """Generate associated texts."""
        return TexteAssocieFactory.batch(size=2)


class NomenclatureFactory(ModelFactory[Nomenclature]):
    """Factory for Nomenclature."""

    __model__ = Nomenclature

    @classmethod
    def referentielNoyau(cls) -> str:
        """Generate core reference."""
        return "CORPS"

    @classmethod
    def typeReferentiel(cls) -> str:
        """Generate reference type."""
        return "A"

    @classmethod
    def repertoireHRAccess(cls) -> str:
        """Generate HR Access directory."""
        return "E22"

    @classmethod
    def code(cls) -> str:
        """Generate code."""
        return "00003"


class VersionCouranteFactory(ModelFactory[VersionCourante]):
    """Factory for VersionCourante."""

    __model__ = VersionCourante

    @classmethod
    def version(cls) -> str:
        """Generate version."""
        return "23.10.01"

    @classmethod
    def type(cls) -> str:
        """Generate type."""
        return "U"

    @classmethod
    def status(cls) -> str:
        """Generate status."""
        return "D"


class SyntheseEvenementsFactory(ModelFactory[SyntheseEvenements]):
    """Factory for SyntheseEvenements."""

    __model__ = SyntheseEvenements

    @classmethod
    def typeMiseAJourGlobale(cls) -> str:
        """Generate global update type."""
        return "M"

    @classmethod
    def statusGlobal(cls) -> str:
        """Generate global status."""
        return "1"

    @classmethod
    def versionCreation(cls) -> str:
        """Generate creation version."""
        return "00.05.10"


class EvenementSurCodeFactory(ModelFactory[EvenementSurCode]):
    """Factory for EvenementSurCode."""

    __model__ = EvenementSurCode

    @classmethod
    def versionNoyau(cls) -> str:
        """Generate core version."""
        return "23.10.01"

    @classmethod
    def status(cls) -> str:
        """Generate status."""
        return "1"

    @classmethod
    def typeMiseAJour(cls) -> str:
        """Generate update type."""
        return "M"

    @classmethod
    def utilisateur(cls) -> str:
        """Generate user."""
        return "UPMEUNIER.INT"

    @classmethod
    def nombreAttributs(cls) -> str:
        """Generate number of attributes."""
        return "0"

    @classmethod
    def horodatageMiseAJour(cls) -> str:
        """Generate update timestamp."""
        return "2023-09-07T13:17:50Z"


class EvenementsSurCodeFactory(ModelFactory[EvenementsSurCode]):
    """Factory for EvenementsSurCode."""

    __model__ = EvenementsSurCode

    nomenclature = NomenclatureFactory
    versionCourante = VersionCouranteFactory
    syntheseDesEvenements = SyntheseEvenementsFactory

    @classmethod
    def evenementsSurCode(cls) -> List[EvenementSurCode]:
        """Generate events on code."""
        return EvenementSurCodeFactory.batch(size=2)


class CorpsOuPseudoCorpsFactory(ModelFactory[CorpsOuPseudoCorps]):
    """Factory for CorpsOuPseudoCorps."""

    __model__ = CorpsOuPseudoCorps

    libelles = LibellesFactory
    validite = ValiditeFactory
    validiteJuridique = ValiditeJuridiqueFactory
    caracteristiques = CaracteristiquesFactory

    @classmethod
    def sousCategorie(cls) -> List[SousCategorie]:
        """Generate subcategories."""
        return SousCategorieFactory.batch(size=1)

    @classmethod
    def ministereEtInstitutionDeLaRepublique(cls) -> List[MinistereInstitution]:
        """Generate ministries and institutions."""
        return MinistereInstitutionFactory.batch(size=1)

    @classmethod
    def dureeDeStageParModeAccesAuCorps(cls) -> List[DureeStage]:
        """Generate internship durations by corps access mode."""
        return DureeStageFactory.batch(size=3)


class IngresCorpsDocumentFactory(ModelFactory[IngresCorpsDocument]):
    """Factory for IngresCorpsDocument."""

    __model__ = IngresCorpsDocument

    corpsOuPseudoCorps = CorpsOuPseudoCorpsFactory
    evenementsSurCode = EvenementsSurCodeFactory
    definitionsHistoriques = DefinitionsHistoriquesFactory

    @classmethod
    def identifiant(cls) -> str:
        """Generate unique identifier."""
        return str(uuid.uuid4().int)[:5].zfill(5)


class IngresCorpsApiResponseFactory(ModelFactory[IngresCorpsApiResponse]):
    """Factory for IngresCorpsApiResponse."""

    __model__ = IngresCorpsApiResponse

    @classmethod
    def documents(cls) -> List[IngresCorpsDocument]:
        """Generate documents."""
        return IngresCorpsDocumentFactory.batch(size=4)
