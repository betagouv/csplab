import uuid
from typing import List

from polyfactory.factories.pydantic_factory import ModelFactory

from infrastructure.external_gateways.dtos.ingres_corps_dtos import (
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
    __model__ = Libelles

    @classmethod
    def libelleCourt(cls) -> str:
        return "PROF LYCE PROF AGRI"

    @classmethod
    def libelleLong(cls) -> str:
        return "Professeurs de lycée professionnel agricole"

    @classmethod
    def libelleImpression(cls) -> str:
        return "Professeurs de lycée professionnel agricole"


class ValiditeFactory(ModelFactory[Validite]):
    __model__ = Validite

    @classmethod
    def status(cls) -> str:
        return "A"

    @classmethod
    def debutValidite(cls) -> str:
        return "1989-09-01T00:00:00Z"


class ValiditeJuridiqueFactory(ModelFactory[ValiditeJuridique]):
    __model__ = ValiditeJuridique


class NatureDeCorpsFactory(ModelFactory[NatureDeCorps]):
    __model__ = NatureDeCorps

    @classmethod
    def codeCorps(cls) -> str:
        return "3"

    @classmethod
    def libelleCorps(cls) -> str:
        return "Spécifique"


class PopulationFactory(ModelFactory[Population]):
    __model__ = Population

    @classmethod
    def codePopulation(cls) -> str:
        return "1"

    @classmethod
    def libellePopulation(cls) -> str:
        return "Fonctionnaire"


class CategorieFactory(ModelFactory[Categorie]):
    __model__ = Categorie

    @classmethod
    def codeCategorie(cls) -> str:
        return "1"

    @classmethod
    def libelleCategorie(cls) -> str:
        return "catégorie A"


class FiliereFactory(ModelFactory[Filiere]):
    __model__ = Filiere


class NiveauDiplomeFactory(ModelFactory[NiveauDiplome]):
    __model__ = NiveauDiplome

    @classmethod
    def codeNiveauDiplome(cls) -> str:
        return "G"

    @classmethod
    def libelleNiveauDiplome(cls) -> str:
        return "Niveau 7 Master/diplômes équivalents"


class NatureFonctionPubliqueFactory(ModelFactory[NatureFonctionPublique]):
    __model__ = NatureFonctionPublique

    @classmethod
    def codeNatureFoncPub(cls) -> str:
        return "1"

    @classmethod
    def libelleNatureFoncPub(cls) -> str:
        return "FPE"


class CorpsGeneriqueFactory(ModelFactory[CorpsGenerique]):
    __model__ = CorpsGenerique

    @classmethod
    def codeCorpsGenerique(cls) -> str:
        return "00016"

    @classmethod
    def libelleCorpsGenerique(cls) -> str:
        return "CG PROF UNIV ET ASSI"


class CaracteristiquesFactory(ModelFactory[Caracteristiques]):
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
        return "0"

    @classmethod
    def corpsExtinction(cls) -> str:
        return "0"


class SousCategorieFactory(ModelFactory[SousCategorie]):
    __model__ = SousCategorie

    @classmethod
    def dateEffet(cls) -> str:
        return "1989-10-01T00:00:00Z"

    @classmethod
    def codeSousCategorie(cls) -> str:
        return "1"

    @classmethod
    def libelleSousCategorie(cls) -> str:
        return "A+"


class MinistereInstitutionFactory(ModelFactory[MinistereInstitution]):
    __model__ = MinistereInstitution

    @classmethod
    def codeMinistere(cls) -> str:
        return "MI130"

    @classmethod
    def libelleMinistere(cls) -> str:
        return "MAA"


class ModeAccesCorpsFactory(ModelFactory[ModeAccesCorps]):
    __model__ = ModeAccesCorps

    @classmethod
    def codeModeAccesCorps(cls) -> str:
        return "AC101"

    @classmethod
    def libelleModeAccesCorps(cls) -> str:
        return "Concours externe"


class DureeStageFactory(ModelFactory[DureeStage]):
    __model__ = DureeStage

    modeAccesCorps = ModeAccesCorpsFactory

    @classmethod
    def dateDebut(cls) -> str:
        return "1989-09-01T00:00:00Z"

    @classmethod
    def dureeStageAnnees(cls) -> str:
        return "1"

    @classmethod
    def dureeStageMois(cls) -> str:
        return "0"


class TypeTexteFactory(ModelFactory[TypeTexte]):
    __model__ = TypeTexte

    @classmethod
    def codeType(cls) -> str:
        return "01"

    @classmethod
    def libelleType(cls) -> str:
        return "Décret"


class NatureTexteFactory(ModelFactory[NatureTexte]):
    __model__ = NatureTexte

    @classmethod
    def codeNature(cls) -> str:
        return "1"

    @classmethod
    def libelleNature(cls) -> str:
        return "Texte d'origine"


class TexteAssocieFactory(ModelFactory[TexteAssocie]):
    __model__ = TexteAssocie

    type = TypeTexteFactory
    nature = NatureTexteFactory

    @classmethod
    def identifiant(cls) -> str:
        return "00000000071"

    @classmethod
    def numeroTexte(cls) -> str:
        return "90-90"

    @classmethod
    def dateTexte(cls) -> str:
        return "1990-01-24T00:00:00Z"

    @classmethod
    def datePublication(cls) -> str:
        return "1990-01-24T00:00:00Z"

    @classmethod
    def NOR(cls) -> str:
        return "AGRA8902379D"

    @classmethod
    def legiFrance(cls) -> str:
        return "JORFTEXT000000707201"

    @classmethod
    def descriptif(cls) -> str:
        return (
            "Décret n° 90-90 du 24 janvier 1990 relatif au statut particulier "
            "des professeurs de lycée professionnel agricole"
        )


class DefinitionsHistoriquesFactory(ModelFactory[DefinitionsHistoriques]):
    __model__ = DefinitionsHistoriques

    @classmethod
    def textesAssocies(cls) -> List[TexteAssocie]:
        return TexteAssocieFactory.batch(size=2)


class NomenclatureFactory(ModelFactory[Nomenclature]):
    __model__ = Nomenclature

    @classmethod
    def referentielNoyau(cls) -> str:
        return "CORPS"

    @classmethod
    def typeReferentiel(cls) -> str:
        return "A"

    @classmethod
    def repertoireHRAccess(cls) -> str:
        return "E22"

    @classmethod
    def code(cls) -> str:
        return "00003"


class VersionCouranteFactory(ModelFactory[VersionCourante]):
    __model__ = VersionCourante

    @classmethod
    def version(cls) -> str:
        return "23.10.01"

    @classmethod
    def type(cls) -> str:
        return "U"

    @classmethod
    def status(cls) -> str:
        return "D"


class SyntheseEvenementsFactory(ModelFactory[SyntheseEvenements]):
    __model__ = SyntheseEvenements

    @classmethod
    def typeMiseAJourGlobale(cls) -> str:
        return "M"

    @classmethod
    def statusGlobal(cls) -> str:
        return "1"

    @classmethod
    def versionCreation(cls) -> str:
        return "00.05.10"


class EvenementSurCodeFactory(ModelFactory[EvenementSurCode]):
    __model__ = EvenementSurCode

    @classmethod
    def versionNoyau(cls) -> str:
        return "23.10.01"

    @classmethod
    def status(cls) -> str:
        return "1"

    @classmethod
    def typeMiseAJour(cls) -> str:
        return "M"

    @classmethod
    def utilisateur(cls) -> str:
        return "UPMEUNIER.INT"

    @classmethod
    def nombreAttributs(cls) -> str:
        return "0"

    @classmethod
    def horodatageMiseAJour(cls) -> str:
        return "2023-09-07T13:17:50Z"


class EvenementsSurCodeFactory(ModelFactory[EvenementsSurCode]):
    __model__ = EvenementsSurCode

    nomenclature = NomenclatureFactory
    versionCourante = VersionCouranteFactory
    syntheseDesEvenements = SyntheseEvenementsFactory

    @classmethod
    def evenementsSurCode(cls) -> List[EvenementSurCode]:
        return EvenementSurCodeFactory.batch(size=2)


class CorpsOuPseudoCorpsFactory(ModelFactory[CorpsOuPseudoCorps]):
    __model__ = CorpsOuPseudoCorps

    libelles = LibellesFactory
    validite = ValiditeFactory
    validiteJuridique = ValiditeJuridiqueFactory
    caracteristiques = CaracteristiquesFactory

    @classmethod
    def sousCategorie(cls) -> List[SousCategorie]:
        return SousCategorieFactory.batch(size=1)

    @classmethod
    def ministereEtInstitutionDeLaRepublique(cls) -> List[MinistereInstitution]:
        return MinistereInstitutionFactory.batch(size=1)

    @classmethod
    def dureeDeStageParModeAccesAuCorps(cls) -> List[DureeStage]:
        return DureeStageFactory.batch(size=3)


class IngresCorpsDocumentFactory(ModelFactory[IngresCorpsDocument]):
    __model__ = IngresCorpsDocument

    corpsOuPseudoCorps = CorpsOuPseudoCorpsFactory
    evenementsSurCode = EvenementsSurCodeFactory
    definitionsHistoriques = DefinitionsHistoriquesFactory

    @classmethod
    def identifiant(cls) -> str:
        return str(uuid.uuid4().int)[:5].zfill(5)


class IngresCorpsApiResponseFactory(ModelFactory[IngresCorpsApiResponse]):
    __model__ = IngresCorpsApiResponse

    @classmethod
    def documents(cls) -> List[IngresCorpsDocument]:
        """Generate documents."""
        return IngresCorpsDocumentFactory.batch(size=4)
