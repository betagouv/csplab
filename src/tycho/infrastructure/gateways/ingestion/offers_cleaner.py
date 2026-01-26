"""Offers cleaner adapter."""

from datetime import datetime
from typing import List, Optional

import polars as pl
from pydantic import HttpUrl

from domain.entities.document import Document, DocumentType
from domain.entities.offer import Offer
from domain.exceptions.document_error import InvalidDocumentTypeError
from domain.services.document_cleaner_interface import IDocumentCleaner
from domain.services.logger_interface import ILogger
from domain.value_objects.contract_type import ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse


class OffersCleaner(IDocumentCleaner[Offer]):
    """Adapter for cleaning raw documents of type OFFERS into Offers entities."""

    def __init__(self, logger: ILogger):
        """Initialize with logger dependency."""
        self.logger = logger.get_logger("OffersCleaner::clean")

    def clean(self, raw_documents: List[Document]) -> List[Offer]:
        """Clean raw documents and return Offers entities."""
        if not raw_documents:
            return []

        for document in raw_documents:
            if document.type != DocumentType.OFFERS:
                raise InvalidDocumentTypeError(document.type.value)

        offers_data = []
        for document in raw_documents:
            parsed_data = self._parse_offer_data(document.raw_data)
            if parsed_data:
                offers_data.append(parsed_data)

        if not offers_data:
            return []

        df = pl.DataFrame(offers_data)
        df_filtered = self._apply_filters(df)

        return self._dataframe_to_offers(df_filtered)

    def _parse_offer_data(self, raw_data: dict) -> Optional[dict]:
        """Parse raw offer data into structured format."""
        item = raw_data

        # Handle optional salaryRange field for verse
        verse = None
        salary_range = item.get("salaryRange")
        if salary_range and salary_range.get("clientCode"):
            verse = salary_range["clientCode"]

        # Contract type
        contract_type = None
        contract_type_object = item.get("contractType")
        if contract_type_object and contract_type_object.get("clientCode"):
            contract_type = contract_type_object["clientCode"]

        # Category from offerFamilyCategory
        category = None
        offer_family_category = item.get("offerFamilyCategory")
        if offer_family_category and offer_family_category.get("clientCode"):
            category = offer_family_category["clientCode"]

        # Handle optional country field
        country = None
        if item.get("country") and len(item["country"]) == 1:
            country = item["country"][0]["clientCode"]

        # Handle optional region field
        region = None
        if item.get("region") and len(item["region"]) == 1:
            region = item["region"][0]["clientCode"]

        # Handle optional department field
        department = None
        if item.get("department") and len(item["department"]) == 1:
            department = item["department"][0]["clientCode"]

        return {
            "external_id": item["reference"],
            "verse": verse,
            "category": category,
            "contract_type": contract_type,
            "title": item.get("title"),
            "mission": item.get("description1"),
            "profile": item.get("description2"),
            "organisation": item.get("organisationName"),
            "country": country,
            "region": region,
            "department": department,
            "offer_url": item.get("offerUrl"),
            "publication_date": item.get("startPublicationDate"),
            "beginning_date": item.get("beginningDate"),
        }

    def _apply_filters(self, df: pl.DataFrame) -> pl.DataFrame:
        """Apply filters to keep only valid offers."""
        # Filter out offers without required fields
        required_fields = ["external_id", "title", "organisation", "publication_date"]
        for field in required_fields:
            df = df.filter(pl.col(field).is_not_null())
            df = df.filter(pl.col(field) != "")

        return df

    def _dataframe_to_offers(self, df: pl.DataFrame) -> List[Offer]:
        """Convert processed DataFrame to Offer entities."""
        if len(df) == 0:
            return []

        offers_list = []
        for _, row in enumerate(df.to_dicts()):
            verse = None
            salary_range = row.get("salaryRange")
            if salary_range and salary_range.get("clientCode"):
                verse = salary_range["clientCode"]

            contract_type = self._map_contract_type(row["contract_type"])

            country = None
            if row.get("country") and len(row["country"]) == 1:
                country = row["country"][0]["clientCode"]

            region = None
            if row.get("region") and len(row["region"]) == 1:
                region = row["region"][0]["clientCode"]

            department = None
            if row.get("department") and len(row["department"]) == 1:
                department = row["department"][0]["clientCode"]

            localisation = self._map_localisation(country, region, department)
            offer_url = self._parse_url(row["offer_url"])
            publication_date = self._parse_publication_date(row["publication_date"])
            beginning_date = self._parse_beginning_date(row["beginning_date"])

            offer_id = hash(row["external_id"]) % (10**9)  # todo: better id generation

            offer = Offer(
                id=offer_id,
                external_id=row["external_id"],
                verse=verse,
                title=row["title"],
                profile=row["profile"] or "",
                mission=row["mission"] or "",
                category=None,  # todo
                contract_type=contract_type,
                organization=row["organisation"],
                offer_url=offer_url,
                localisation=localisation,
                publication_date=publication_date,
                beginning_date=beginning_date,
            )
            offers_list.append(offer)

        return offers_list

    def _map_verse(self, verse_str: Optional[str]) -> Verse:
        """Map verse string to Verse enum."""
        if not verse_str:
            return Verse.FPE  # Default value

        if "FPT" in verse_str:
            return Verse.FPT
        elif "FPE" in verse_str:
            return Verse.FPE
        else:
            return Verse.FPH

    def _map_contract_type(
        self, contract_type_str: Optional[str]
    ) -> Optional[ContractType]:
        """Map contract type string to ContractType enum."""
        if not contract_type_str:
            return None

        contract_upper = contract_type_str.upper()
        if "TITULAIRE" in contract_upper:
            return ContractType.TITULAIRE_CONTRACTUEL
        elif "CONTRACTUEL" in contract_upper:
            return ContractType.CONTRACTUELS
        elif "TERRITORIAL" in contract_upper:
            return ContractType.TERRITORIAL
        else:
            return None

    def _map_localisation(
        self, country: Optional[str], region: Optional[str], department: Optional[str]
    ) -> Optional[Localisation]:
        """Map location fields to Localisation value object."""
        if not country or not region or not department:
            return None

        return Localisation(
            country=Country(country),
            region=Region(code=region),
            department=Department(code=department),
        )

    def _parse_url(self, url_str: Optional[str]) -> Optional[HttpUrl]:
        """Parse URL string to HttpUrl."""
        if not url_str:
            return None

        return HttpUrl(url_str)

    def _parse_publication_date(self, date_str: Optional[str]) -> datetime:
        """Parse publication date string to timezone-aware datetime."""
        if not date_str:
            return datetime.now()

        try:
            return datetime.fromisoformat(date_str)
        except (ValueError, TypeError):
            return datetime.now()

    def _parse_beginning_date(self, date_str: Optional[str]) -> Optional[LimitDate]:
        """Parse beginning date string to LimitDate."""
        if not date_str:
            return None

        try:
            parsed_date = datetime.fromisoformat(date_str)
            return LimitDate(value=parsed_date)
        except (ValueError, TypeError):
            return None
