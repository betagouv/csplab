"""Offers cleaner adapter with TalentSoft DTO validation."""

from datetime import datetime
from typing import List, Optional

from pydantic import HttpUrl, ValidationError

from domain.entities.document import Document, DocumentType
from domain.entities.offer import Offer
from domain.exceptions.document_error import InvalidDocumentTypeError
from domain.exceptions.offer_errors import InvalidOfferDataFormatError
from domain.services.document_cleaner_interface import IDocumentCleaner
from domain.services.logger_interface import ILogger
from domain.value_objects.contract_type import ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse
from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftOffer,
)


class OffersCleaner(IDocumentCleaner[Offer]):
    """Adapter for cleaning raw documents of type OFFERS into Offers entities."""

    def __init__(self, logger: ILogger):
        """Initialize with logger dependency."""
        self.logger = logger.get_logger("OffersCleaner::clean")

    def clean(self, raw_documents: List[Document]) -> List[Offer]:
        """Clean raw documents and return Offers entities."""
        for document in raw_documents:
            if document.type != DocumentType.OFFERS:
                raise InvalidDocumentTypeError(document.type.value)  # todo: test

        validated_offers = []
        for document in raw_documents:
            try:
                talentsoft_offer = TalentsoftOffer.model_validate(document.raw_data)

                validated_offers.append(talentsoft_offer)
            except ValidationError as e:  # todo: test
                reference = document.raw_data.get("reference", "UNKNOWN")
                self.logger.error(f"TalentSoft validation failed for offer {reference}")
                raise InvalidOfferDataFormatError(reference, str(e)) from e

        if not validated_offers:
            return []  # todo: test

        offers_list = []
        for talentsoft_offer in validated_offers:
            try:
                offer = self._map_talentsoft_to_offer(talentsoft_offer)
                offers_list.append(offer)
            except (ValueError, ValidationError) as e:
                self.logger.error(
                    f"Value object validation failed for offer"
                    f"{talentsoft_offer.reference}: {e}"
                )
                # Continue sans ajouter cette offre à la liste
                continue

        return offers_list

    def _map_talentsoft_to_offer(self, talentsoft_offer: TalentsoftOffer) -> Offer:
        """Map a validated TalentSoft DTO to an Offer entity."""
        # Extract verse from salaryRange if available
        verse = self._map_verse(
            talentsoft_offer.salaryRange.clientCode
            if talentsoft_offer.salaryRange
            else None
        )

        # Map contract type
        contract_type = self._map_contract_type(
            talentsoft_offer.contractType.clientCode
            if talentsoft_offer.contractType
            else None
        )

        # Map localisation from geographical arrays
        localisation = self._map_localisation_from_arrays(
            talentsoft_offer.country,
            talentsoft_offer.region,
            talentsoft_offer.department,
        )

        # Parse URLs and dates
        offer_url = self._parse_url(talentsoft_offer.offerUrl)
        publication_date = self._parse_publication_date(
            talentsoft_offer.startPublicationDate
        )
        beginning_date = self._parse_beginning_date(talentsoft_offer.beginningDate)

        # Generate consistent ID from reference
        offer_id = hash(talentsoft_offer.reference) % (10**9)

        return Offer(
            id=offer_id,
            external_id=talentsoft_offer.reference,
            verse=verse,
            title=talentsoft_offer.title,
            profile=talentsoft_offer.description2 or "",
            mission=talentsoft_offer.description1 or "",
            category=None,  # TODO: Map from offerFamilyCategory if needed
            contract_type=contract_type,
            organization=talentsoft_offer.organisationName,
            offer_url=offer_url,
            localisation=localisation,
            publication_date=publication_date,
            beginning_date=beginning_date,
        )

    def _map_verse(self, verse_str: Optional[str]) -> Verse:
        """Map verse string to Verse enum."""
        if not verse_str:
            return Verse.FPE  # Default value

        verse_upper = verse_str.upper()
        if "FPT" in verse_upper:
            return Verse.FPT  # todo: test
        elif "FPH" in verse_upper:
            return Verse.FPH  # todo: test
        else:
            return Verse.FPE

    def _map_contract_type(
        self, contract_type_str: Optional[str]
    ) -> Optional[ContractType]:
        """Map contract type string to ContractType enum."""
        if not contract_type_str:
            return None  # todo: test

        contract_upper = contract_type_str.upper()
        if "TITULAIRE" in contract_upper:
            return ContractType.TITULAIRE_CONTRACTUEL
        elif "CONTRACTUEL" in contract_upper:
            return ContractType.CONTRACTUELS
        elif "TERRITORIAL" in contract_upper:  # todo: test
            return ContractType.TERRITORIAL
        else:
            return None  # todo: test

    def _map_localisation_from_arrays(
        self, countries: List, regions: List, departments: List
    ) -> Optional[Localisation]:
        """Map location arrays to Localisation value object."""
        # Extract first element from each array if available
        country_code = countries[0].clientCode if countries else None
        region_code = regions[0].clientCode if regions else None
        department_code = departments[0].clientCode if departments else None

        if not country_code or not region_code or not department_code:
            return None  # todo: test

        # Transform TalentSoft codes to INSEE codes
        # Region codes: R24 -> 24
        insee_region_code = (
            region_code.lstrip("R") if region_code.startswith("R") else region_code
        )

        return Localisation(
            country=Country(country_code),
            region=Region(code=insee_region_code),
            department=Department(code=department_code),
        )

    def _parse_url(self, url_str: Optional[str]) -> Optional[HttpUrl]:
        """Parse URL string to HttpUrl."""
        if not url_str:
            return None  # todo: test

        try:
            return HttpUrl(url_str)
        except Exception:
            return None  # todo: test

    def _parse_publication_date(self, date_str: str) -> datetime:
        """Parse publication date string to timezone-aware datetime."""
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, TypeError, AttributeError):  # todo: test
            return datetime.now()

    def _parse_beginning_date(self, date_str: Optional[str]) -> Optional[LimitDate]:
        """Parse beginning date string to LimitDate."""
        if not date_str:
            return None  # todo: test

        try:
            parsed_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return LimitDate(value=parsed_date)
        except (ValueError, TypeError, AttributeError):
            return None  # todo: test
