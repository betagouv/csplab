from typing import List, Optional
from uuid import UUID, uuid4

from faker import Faker
from polyfactory.factories import DataclassFactory

from domain.entities.metier import Metier
from domain.value_objects.verse import Verse
from infrastructure.django_apps.shared.models.metier import MetierModel

fake = Faker()


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

    @staticmethod
    def create_model(
        id: Optional[UUID] = None,
        external_id: Optional[str] = None,
        libelle_long: Optional[str] = None,
        definition_synthetique: Optional[str] = None,
        code_domaine_fonctionnel: Optional[str] = None,
        offer_family_code: Optional[str] = None,
        versants: Optional[List[Verse]] = None,
        activites: Optional[List[str]] = None,
        conditions_particulieres: Optional[List[str]] = None,
    ) -> MetierModel:
        if id is None:
            id = uuid4()

        if external_id is None:
            external_id = str(id)[:8]

        if libelle_long is None:
            libelle_long = fake.word()

        if definition_synthetique is None:
            definition_synthetique = fake.sentence()

        if code_domaine_fonctionnel is None:
            code_domaine_fonctionnel = fake.random_element(["JUR", "TRA", "MED"])

        if offer_family_code is None:
            offer_family_code = fake.bothify("????????").upper()

        if versants is None:
            versants = [Verse.FPE, Verse.FPT]

        if activites is None:
            activites = []
            activites.append(
                fake.sentence(),
            )

        if conditions_particulieres is None:
            conditions_particulieres = [fake.sentence()]

        versants_values = [verse.value for verse in versants] if versants else None

        return MetierModel(
            id=id,
            external_id=external_id,
            libelle_long=libelle_long,
            definition_synthetique=definition_synthetique,
            code_domaine_fonctionnel=code_domaine_fonctionnel,
            offer_family_code=offer_family_code,
            versants=versants_values,
            conditions_particulieres=conditions_particulieres,
            activites=activites,
        )
