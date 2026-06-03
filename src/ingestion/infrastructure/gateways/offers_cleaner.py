import logging
from datetime import datetime
from typing import List, Optional, cast

from pydantic import HttpUrl, ValidationError

from domain.entities.offer import Offer
from domain.entities.raw_offer import RawOffer
from domain.value_objects.area import GeographicalArea
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region
from domain.value_objects.verse import Verse
from infrastructure.external_gateways.dtos.talentsoft_dtos import TalentsoftDetailOffer

logger = logging.getLogger(__name__)

_TALENTSOFT_TO_AREA: dict[str, GeographicalArea] = {
    "_TS_CO_GeographicalArea_Afrique": GeographicalArea.AFRIQUE,
    "_TS_CO_GeographicalArea_AmriquesCaraibe": GeographicalArea.AMERIQUE,
    "_TS_CO_GeographicalArea_Asie": GeographicalArea.ASIE,
    "_TS_CO_GeographicalArea_Europe": GeographicalArea.EUROPE,
    "_TS_CO_GeographicalArea_MoyenOrientAfriqueduNord": GeographicalArea.AFRIQUE,
    "_TS_CO_GeographicalArea_Ocanie": GeographicalArea.OCEANIE,
}


class OffersCleaner:
    def clean(self, raw_offer: RawOffer) -> Offer:
        if not raw_offer.data:
            raise ValueError(f"RawOffer {raw_offer.reference} has no data to clean")
        if not raw_offer.source_id:
            raise ValueError(f"RawOffer {raw_offer.reference} has no source_id")

        talentsoft_offer = TalentsoftDetailOffer.model_validate(raw_offer.data)
        return self._map_talentsoft_to_offer(talentsoft_offer, raw_offer)

    def _map_talentsoft_to_offer(
        self, talentsoft_offer: TalentsoftDetailOffer, raw_offer: RawOffer
    ) -> Offer:
        ts_verse = (
            talentsoft_offer.salaryRange.clientCode
            if talentsoft_offer.salaryRange
            else "UNK"
        )
        verse = self._map_verse(ts_verse, talentsoft_offer.reference)

        contract_type = self._map_contract_type(
            talentsoft_offer.contractType.clientCode
            if talentsoft_offer.contractType
            else None
        )

        localisation = self._map_localisation_from_arrays(
            talentsoft_offer.geographicalLocation,
            talentsoft_offer.country,
            talentsoft_offer.region,
            talentsoft_offer.department,
        )

        offer_url = self._parse_url(talentsoft_offer.offerUrl)
        publication_date = self._parse_publication_date(
            talentsoft_offer.startPublicationDate
        )
        beginning_date = self._parse_beginning_date(talentsoft_offer.beginningDate)

        category = self._parse_category(
            talentsoft_offer.customFields.description.customCodeTable1.clientCode
            if talentsoft_offer.customFields
            and talentsoft_offer.customFields.description
            and talentsoft_offer.customFields.description.customCodeTable1
            else None
        )

        family_code_value = None
        if talentsoft_offer.offerFamilyCategory:
            family_code_value = talentsoft_offer.offerFamilyCategory.clientCode

        return Offer(
            reference=raw_offer.reference,
            source_id=cast(str, raw_offer.source_id),  # guaranteed by clean()
            external_id=f"{ts_verse}-{talentsoft_offer.reference}"
            if ts_verse
            else talentsoft_offer.reference,
            verse=verse,
            title=talentsoft_offer.title,
            profile=talentsoft_offer.description2 or "",
            mission=talentsoft_offer.description1 or "",
            category=category,
            contract_type=contract_type,
            organization=talentsoft_offer.organisationName,
            offer_url=offer_url,
            localisation=localisation,
            publication_date=publication_date,
            beginning_date=beginning_date,
            family_code=family_code_value,
        )

    def _map_verse(self, verse_str: Optional[str], reference: str) -> Optional[Verse]:
        if not verse_str:
            return None
        verse_upper = verse_str.upper()
        if "FPT" in verse_upper:
            return Verse.FPT
        elif "FPH" in verse_upper or "APHP" in reference.upper():
            return Verse.FPH
        elif "FPE" in verse_upper:
            return Verse.FPE
        return None

    def _map_contract_type(
        self, contract_type_str: Optional[str]
    ) -> Optional[ContractType]:
        if not contract_type_str:
            return None

        contract_upper = contract_type_str.upper()
        if "TITULAIRE" in contract_upper:
            return ContractType.TITULAIRE_CONTRACTUEL
        elif "CONTRACTUEL" in contract_upper:
            return ContractType.CONTRACTUELS
        elif "TERRITORIAL" in contract_upper:
            return ContractType.TERRITORIAL

        return None

    def _map_localisation_from_arrays(
        self, areas: List, countries: List, regions: List, departments: List
    ) -> Optional[Localisation]:
        area_code = areas[0].clientCode if areas else None
        country_code = countries[0].clientCode if countries else None
        region_code = regions[0].clientCode if regions else None
        department_code = departments[0].clientCode if departments else None

        if not country_code or not region_code or not department_code or not area_code:
            return None

        area = _TALENTSOFT_TO_AREA.get(area_code)
        if area is None:
            return None

        if region_code.startswith("_TS_CO_Region_"):
            insee_region_code = region_code.replace("_TS_CO_Region_", "")
        elif region_code.startswith("R"):
            insee_region_code = region_code.lstrip("R")
        else:
            insee_region_code = region_code

        if department_code.startswith("_TS_CO_Department_NouvelleCaldonie988"):
            insee_department_code = "988"
        else:
            insee_department_code = department_code

        try:
            return Localisation(
                area=area,
                country=Country(country_code),
                region=Region(code=insee_region_code),
                department=Department(code=insee_department_code),
            )
        except (ValueError, ValidationError) as e:
            logger.warning(
                "Invalid localisation for region=%s department=%s: %s",
                region_code,
                department_code,
                e,
            )
            return None

    def _parse_url(self, url_str: str) -> Optional[HttpUrl]:
        try:
            return HttpUrl(url_str)
        except Exception:
            return None

    def _parse_publication_date(self, date_str: str) -> datetime:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))

    def _parse_beginning_date(self, date_str: Optional[str]) -> Optional[LimitDate]:
        if not date_str:
            return None

        try:
            parsed_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return LimitDate(value=parsed_date)
        except (ValueError, TypeError, AttributeError):
            return None

    def _parse_category(self, category_code: Optional[str]) -> Optional[Category]:
        if category_code in ["CAT-AEF", "CAT-ESD", "CAT-ES"]:
            return Category.APLUS
        elif category_code == "CAT-A":
            return Category.A
        elif category_code == "CAT-B":
            return Category.B
        elif category_code == "CAT-C":
            return Category.C
        return None
