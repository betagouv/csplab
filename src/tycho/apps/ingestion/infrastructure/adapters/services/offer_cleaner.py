"""Offer cleaner adapter."""

from datetime import datetime
from typing import List, Optional

from core.entities.document import Document, DocumentType
from core.entities.offer import Offer
from core.errors.document_error import InvalidDocumentTypeError
from core.services.document_cleaner_interface import IDocumentCleaner
from core.services.logger_interface import ILogger
from core.value_objects.category import Category
from core.value_objects.department import Department
from core.value_objects.limit_date import LimitDate
from core.value_objects.localisation import Localisation
from core.value_objects.region import Region
from core.value_objects.verse import Verse


class OfferCleaner(IDocumentCleaner[Offer]):
    """Adapter for cleaning raw documents of type OFFER into Offer entities."""

    def __init__(self, logger: ILogger):
        """Initialize with logger dependency."""
        self.logger = logger.get_logger("OfferCleaner::clean")

    def clean(self, raw_documents: List[Document]) -> List[Offer]:
        """Clean raw documents and return Offer entities."""
        for document in raw_documents:
            if document.type != DocumentType.OFFER:
                raise InvalidDocumentTypeError(document.type.value)

        offers = []
        for document in raw_documents:
            try:
                offer = self._parse_offer_data(document.raw_data)
                if offer:
                    offers.append(offer)
            except Exception as e:
                self.logger.error(f"Failed to parse offer {document.id}: {str(e)}")
                continue

        self.logger.info(
            f"Successfully cleaned {len(offers)} offers "
            f"from {len(raw_documents)} documents"
        )
        return offers

    def _parse_offer_data(self, raw_data: dict) -> Optional[Offer]:
        """Parse raw offer data into Offer entity."""
        try:
            # Extract basic fields
            external_id = raw_data["id"]
            offer_id = hash(external_id) % (10**9)  # Convert string to int
            title = raw_data["title"]
            profile = raw_data["profile"]

            # Map category
            category = self._map_category(raw_data.get("category"))

            # Map verse
            verse = self._map_verse(raw_data.get("verse"))

            # Map localisation
            localisation = self._map_localisation(
                raw_data.get("region"), raw_data.get("department")
            )

            # Map limit_date
            limit_date = self._map_limit_date(raw_data.get("limit_date"))

            return Offer(
                id=offer_id,
                external_id=external_id,
                verse=verse,
                titre=title,
                profile=profile,
                category=category,
                localisation=localisation,
                limit_date=limit_date,
            )

        except Exception as e:
            self.logger.error(f"Error parsing offer data: {str(e)}")
            return None

    def _map_category(self, category_str: Optional[str]) -> Category:
        """Map category string to Category enum."""
        if not category_str:
            return Category.HORS_CATEGORIE

        category_upper = category_str.upper()
        if category_upper == "A+":
            return Category.APLUS
        elif category_upper == "A":
            return Category.A
        elif category_upper == "B":
            return Category.B
        elif category_upper == "C":
            return Category.C
        else:
            return Category.HORS_CATEGORIE

    def _map_verse(self, verse_str: Optional[str]) -> Verse:
        """Map verse string to Verse enum."""
        if not verse_str:
            return Verse.FPE  # Default to FPE

        verse_upper = verse_str.upper()
        if verse_upper == "FPT":
            return Verse.FPT
        elif verse_upper == "FPE":
            return Verse.FPE
        elif verse_upper == "FPH":
            return Verse.FPH
        else:
            return Verse.FPE  # Default to FPE

    def _map_localisation(
        self, region_str: Optional[str], department_str: Optional[str]
    ) -> Optional[Localisation]:
        """Map region and department strings to Localisation value object."""
        if not region_str or not department_str:
            return None

        try:
            region = Region(region_str)
            department = Department(department_str)
            return Localisation(region=region, department=department)
        except ValueError as e:
            self.logger.warning(
                f"Invalid region/department: {region_str}/{department_str} - {str(e)}"
            )
            return None

    def _map_limit_date(self, limit_date_str: Optional[str]) -> Optional[LimitDate]:
        """Map limit_date string to LimitDate value object."""
        if not limit_date_str:
            return None

        try:
            # Parse ISO format datetime
            dt = datetime.fromisoformat(limit_date_str.replace("Z", "+00:00"))
            return LimitDate(value=dt)
        except ValueError as e:
            self.logger.warning(
                f"Invalid limit_date format: {limit_date_str} - {str(e)}"
            )
            return None
