from typing import List, Optional
from uuid import UUID, uuid4

from faker import Faker
from polyfactory.factories import DataclassFactory

from domain.entities.metier import Metier
from domain.value_objects.verse import Verse

fake = Faker()


class MetierFactory(DataclassFactory[Metier]):
    @staticmethod
    def create_entity(
        id: Optional[UUID] = None,
        libelle: Optional[str] = None,
        description: Optional[str] = None,
        domaine_fonctionnel_id: Optional[UUID] = None,
        versants: Optional[List[Verse]] = None,
        activites: Optional[List[str]] = None,
        conditions_particulieres: Optional[str] = None,
        offer_family_code: Optional[str] = None,
    ) -> Metier:
        if id is None:
            id = uuid4()

        if libelle is None:
            libelle = fake.word()

        if description is None:
            description = fake.sentence()

        if domaine_fonctionnel_id is None:
            domaine_fonctionnel_id = uuid4()

        if versants is None:
            versants = [Verse.FPE, Verse.FPT]

        if activites is None:
            activites = []
            activites.append(
                fake.sentence(),
            )

        if conditions_particulieres is None:
            conditions_particulieres = fake.sentence()

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
            libelle=libelle,
            description=description,
            domaine_fonctionnel_id=domaine_fonctionnel_id,
            versants=versants,
            activites=activites,
            conditions_particulieres=conditions_particulieres,
            offer_family_code=offer_family_code,
        )
