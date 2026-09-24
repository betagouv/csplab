from typing import List, Optional
from uuid import UUID, uuid4

from faker import Faker
from polyfactory.factories import DataclassFactory
from referentiel.entities.metier import Metier
from referentiel.value_objects.verse import Verse

from infrastructure.mappers.metier_mapper import MetierMapper

fake = Faker()

_mapper = MetierMapper()


class MetierFactory(DataclassFactory[Metier]):
    @staticmethod
    def create_entity(
        id: Optional[UUID] = None,
        external_id: Optional[str] = None,
        libelle: Optional[str] = None,
        description: Optional[str] = None,
        domaine_fonctionnel_code: Optional[str] = None,
        versants: Optional[List[Verse]] = None,
        activites: Optional[List[str]] = None,
        conditions_particulieres: Optional[List[str]] = None,
        offer_family_code: Optional[str] = None,
    ) -> Metier:
        if id is None:
            id = uuid4()

        if external_id is None:
            external_id = str(id)[:8]

        if libelle is None:
            libelle = fake.word()

        if description is None:
            description = fake.sentence()

        if domaine_fonctionnel_code is None:
            domaine_fonctionnel_code = fake.random_element(["JUR", "TRA", "MED"])

        if versants is None:
            versants = [Verse.FPE, Verse.FPT]

        if activites is None:
            activites = []
            activites.append(
                fake.sentence(),
            )

        if conditions_particulieres is None:
            conditions_particulieres = [fake.sentence()]

        if offer_family_code is None:
            domains = [
                "JUR",
                "TRA",
                "MED",
                "NUM",
                "DIR",
                "SEC",
                "ENV",
                "BAT",
                "LOG",
                "GRH",
            ]
            domain = fake.random_element(domains)
            number = fake.random_int(min=1, max=999)
            offer_family_code = f"ER{domain}{number:03d}"

        return Metier(
            id=id,
            external_id=external_id,
            libelle=libelle,
            description=description,
            domaine_fonctionnel_code=domaine_fonctionnel_code,
            versants=versants,
            activites=activites,
            conditions_particulieres=conditions_particulieres,
            offer_family_code=offer_family_code,
        )
