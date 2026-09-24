from datetime import date, datetime, timezone
from typing import List
from uuid import UUID, uuid4

from faker import Faker
from referentiel.entities.organisme import Organisme
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.siret import SIRET
from referentiel.value_objects.verse import Verse


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


_fake = Faker("fr_FR")


class OrganismeFactory:
    @staticmethod
    def create_entity(
        entity_id: UUID | None = None,
        nom: str = "Ministère de l'Économie, des Finances et de la Relance",
        versant: Verse = Verse.FPE,
        localisation: Localisation | None = None,
        siret: SIRET | None = None,
        external_id: str | None = None,
        referentiel: str | None = None,
        millesime: str | None = None,
        gestion_ats: bool | None = False,
        date_creation: date | None = None,
        date_derniere_activite: date | None = None,
    ) -> Organisme:
        if not date_creation:
            date_creation = datetime.now(tz=timezone.utc)
        if not date_derniere_activite:
            date_derniere_activite = datetime.now(tz=timezone.utc)
        return Organisme.build(
            entity_id=entity_id or uuid4(),
            nom=nom,
            versant=versant,
            localisation=localisation or make_localisation(),
            siret=siret or SIRET(code=_fake.siret().replace(" ", "")),
            external_id=external_id or str(uuid4()),
            referentiel=referentiel,
            millesime=millesime,
            gestion_ats=gestion_ats,
            date_creation=date_creation,
            date_derniere_activite=date_derniere_activite,
        )

    @staticmethod
    def create_entity_batch(count: int = 3, **kwargs) -> List[Organisme]:
        return [OrganismeFactory.create_entity(**kwargs) for _ in range(count)]
