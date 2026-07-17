from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4

from django.utils import timezone
from faker import Faker
from polyfactory.factories import DataclassFactory
from referentiel.entities.metier import Metier
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.referentiel.models.metier import MetierModel
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

    @staticmethod
    def create_model(
        id: Optional[UUID] = None,
        external_id: Optional[str] = None,
        libelle: Optional[str] = None,
        description: Optional[str] = None,
        domaine_fonctionnel_code: Optional[str] = None,
        versants: Optional[List[Verse]] = None,
        activites: Optional[List[str]] = None,
        conditions_particulieres: Optional[List[str]] = None,
        offer_family_code: Optional[str] = None,
        processing: bool = False,
        processed_at: Optional[datetime] = None,
        archived_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> MetierModel:

        metier = MetierFactory.create_entity(
            id,
            external_id,
            libelle,
            description,
            domaine_fonctionnel_code,
            versants,
            activites,
            conditions_particulieres,
            offer_family_code,
        )

        metier_model = _mapper.from_domain(metier)
        metier_model.processing = processing
        metier_model.processed_at = processed_at
        metier_model.archived_at = archived_at
        if updated_at is not None:
            metier_model.updated_at = updated_at

        metier_model.save()

        if updated_at is not None:
            MetierModel.objects.filter(pk=metier_model.pk).update(
                updated_at=timezone.make_aware(updated_at)
            )
            metier_model.refresh_from_db()

        return metier_model

    @staticmethod
    def create_model_batch(
        size: int,
        **kwargs,
    ) -> List[MetierModel]:
        return [MetierFactory.create_model(**kwargs) for _ in range(size)]
