from datetime import UTC, datetime
from uuid import UUID, uuid4

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

from infrastructure.factories.datetime_utils import as_aware
from infrastructure.mappers.offer_mapper import OfferMapper

_mapper = OfferMapper()


class OfferFactory:
    @staticmethod
    def create_entity(
        title: str | None = None,
        category: Category | None = None,
        contract_type: ContractType | None = None,
        verse: Verse | None = None,
        external_id: str | None = None,
        reference: str | None = None,
        profile: str | None = None,
        mission: str | None = None,
        organization: str | None = None,
        family_code: str | None = None,
        job_family_referential: str | None = None,
        functional_area_code: str | None = None,
        source_id: UUID | None = None,
        offer_url: HttpUrl | None = None,
        localisation: Localisation | None = None,
        publication_date: datetime | None = None,
        beginning_date: LimitDate | None = None,
        archived_at: datetime | None = None,
        criteria: dict | None = None,
        conditions: dict | None = None,
    ) -> Offer:
        if archived_at:
            archived_at = as_aware(archived_at)

        if localisation is None:
            localisation = Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="11"),
                department=Department(code="75"),
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
            job_family_referential=job_family_referential,
            functional_area_code=functional_area_code,
            source_id=source_id or uuid4(),
            criteria=criteria,
            conditions=conditions,
        )
