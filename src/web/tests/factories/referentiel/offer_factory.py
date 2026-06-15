from datetime import UTC, datetime
from typing import List, Optional
from uuid import UUID, uuid4

from django.utils import timezone
from pydantic import HttpUrl
from referentiel.entities.offer import Offer
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from infrastructure.django_apps.ingestion.models.source import SourceModel
from infrastructure.django_apps.referentiel.models.offer import OfferModel
from tests.factories.ingestion.source_factory import SourceFactory


class OfferFactory:
    @staticmethod
    def create_entity(
        title: str | None = None,
        department: str = "75",
        region: str | None = None,
        country: str | None = None,
        area: str | None = None,
        category: Category | None = None,
        contract_type: ContractType | None = None,
        verse: Verse | None = None,
        external_id: str | None = None,
        reference: str | None = None,
        profile: str | None = None,
        mission: str | None = None,
        organization: str | None = None,
        family_code: str | None = None,
        source_id: UUID | None = None,
        offer_url: HttpUrl | None = None,
        localisation: Localisation | None = None,
        publication_date: datetime | None = None,
        beginning_date: LimitDate | None = None,
        archived_at: datetime | None = None,
    ) -> Offer:
        if archived_at:
            archived_at = timezone.make_aware(archived_at)

        if localisation is None and country and region and department:
            localisation = Localisation(
                area=GeographicalArea(area) if area else GeographicalArea.EUROPE,
                country=Country(country),
                region=Region(code=region),
                department=Department(code=department),
            )
        else:
            localisation = Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="11"),
                department=Department(code=department),
            )
        _external_id = external_id or f"OFFER_{uuid4().hex[:8]}"
        return Offer(
            external_id=_external_id,
            reference=reference or str(uuid4()),
            verse=verse or Verse.FPE,
            title=title or "Test Offer Title",
            profile=profile or "Test profile description",
            mission=mission or "Test mission description",
            category=category or Category.A,
            contract_type=contract_type,
            organization=organization or "Test Organization",
            offer_url=offer_url,
            localisation=localisation,
            publication_date=publication_date or datetime(2024, 1, 15, tzinfo=UTC),
            beginning_date=beginning_date
            or LimitDate(datetime(2024, 12, 31, tzinfo=UTC)),
            processed_at=None,
            archived_at=archived_at,
            family_code=family_code,
            source_id=source_id or uuid4(),
        )

    @staticmethod
    def create_model(
        reference: Optional[str] = None,
        external_id: Optional[str] = None,
        title: Optional[str] = None,
        profile: Optional[str] = None,
        mission: Optional[str] = None,
        organization: Optional[str] = None,
        verse: Optional[Verse] = None,
        category: Optional[Category] = None,
        contract_type: Optional[ContractType] = None,
        offer_url: Optional[HttpUrl] = None,
        publication_date: Optional[datetime] = None,
        beginning_date: Optional[LimitDate] = None,
        localisation: Optional[Localisation] = None,
        family_code: Optional[str] = None,
        source_id: Optional[UUID] = None,
        updated_at: Optional[datetime] = None,
        processing: bool = False,
        processed_at: Optional[datetime] = None,
        archived_at: Optional[datetime] = None,
    ) -> OfferModel:
        if processed_at:
            processed_at = timezone.make_aware(processed_at)

        if source_id is None:
            source_id = SourceFactory.create_model().source_id
        elif not SourceModel.objects.filter(source_id=source_id).exists():
            SourceFactory.create_model(source_id=source_id)

        offer = OfferFactory.create_entity(
            reference=reference,
            external_id=external_id,
            verse=verse,
            title=title,
            profile=profile,
            mission=mission,
            category=category,
            contract_type=contract_type,
            organization=organization,
            offer_url=offer_url,
            localisation=localisation,
            family_code=family_code,
            source_id=source_id,
            publication_date=publication_date,
            beginning_date=beginning_date,
            archived_at=archived_at,
        )

        offer_model = OfferModel.from_entity(offer)
        offer_model.processing = processing
        offer_model.processed_at = processed_at
        offer_model.save()

        if updated_at:
            OfferModel.objects.filter(id=offer.id).update(
                updated_at=timezone.make_aware(updated_at)
            )
            offer_model.refresh_from_db()

        return offer_model

    @staticmethod
    def create_model_batch(
        size: int,
        **kwargs,
    ) -> List[OfferModel]:
        return [OfferFactory.create_model(**kwargs) for _ in range(size)]
