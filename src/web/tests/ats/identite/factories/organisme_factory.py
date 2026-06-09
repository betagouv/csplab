from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from domain.identite.entities.organisme import Organisme
from domain.identite.value_objects.siret import SIRET


def make_localisation(
    department: str = "75",
    region: str = "11",
    country: str = "FRA",
) -> Localisation:
    return Localisation(
        area=GeographicalArea.EUROPE,
        country=Country(country),
        region=Region(code=region),
        department=Department(code=department),
    )


class OrganismeFactory:
    @staticmethod
    def build(
        nom: str = "Ministère de l'Économie, des Finances et de la Relance",
        versant: Verse = Verse.FPE,
        localisation: Localisation | None = None,
        siret: SIRET | None = None,
    ) -> Organisme:
        return Organisme.build(
            nom=nom,
            versant=versant,
            localisation=localisation or make_localisation(),
            siret=siret,
        )
