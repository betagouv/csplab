from domain.identite.entities.organisme import Organisme
from domain.identite.value_objects.siret import SIRET
from domain.value_objects.area import GeographicalArea
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse


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
