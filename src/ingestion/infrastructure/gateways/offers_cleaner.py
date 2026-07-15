import logging
from datetime import datetime
from typing import List, Optional, cast
from uuid import UUID

from pydantic import HttpUrl, ValidationError
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractKind, ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language import Language
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from domain.entities.offer import Offer
from domain.entities.raw_offer import RawOffer
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

        contract_kind = self._map_contract_kind(
            talentsoft_offer.customFields.offer.customCodeTable2.clientCode
            if talentsoft_offer.customFields
            and talentsoft_offer.customFields.offer
            and talentsoft_offer.customFields.offer.customCodeTable2
            else None
        )

        localisation = self._map_localisation_from_arrays(
            talentsoft_offer.geographicalLocation,
            talentsoft_offer.country,
            talentsoft_offer.region,
            talentsoft_offer.department,
        )

        offer_url = self._parse_url(talentsoft_offer.offerUrl)
        application_url = (
            self._parse_url(talentsoft_offer.applicationUrl)
            if talentsoft_offer.applicationUrl
            else None
        )
        publication_date = self._parse_publication_date(
            talentsoft_offer.startPublicationDate
        )
        end_publication_date = self._parse_optional_date(
            talentsoft_offer.endPublicationDate
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

        education_level = (
            self._map_education_level(talentsoft_offer.educationLevel.clientCode)
            if talentsoft_offer.educationLevel
            else None
        )

        experience = (
            self._map_experience(talentsoft_offer.experienceLevel.clientCode)
            if talentsoft_offer.experienceLevel
            else None
        )

        specialisations = [s.clientCode for s in talentsoft_offer.specialisations]

        languages = [
            Language(
                iso_code=lang.languageName.clientCode,
                language_level=LanguageLevel(lang.languageLevel.clientCode),
            )
            for lang in talentsoft_offer.languages
        ]

        diploma = (
            talentsoft_offer.diploma.clientCode if talentsoft_offer.diploma else None
        )

        return Offer(
            reference=raw_offer.reference,
            source_id=UUID(cast(str, raw_offer.source_id)),
            external_id=f"{ts_verse}-{talentsoft_offer.reference}"
            if ts_verse
            else talentsoft_offer.reference,
            verse=verse,
            title=talentsoft_offer.title,
            profile=talentsoft_offer.description2 or "",
            mission=talentsoft_offer.description1 or "",
            category=category,
            contract_type=contract_type,
            contract_kind=contract_kind,
            organization=talentsoft_offer.organisationName,
            offer_url=offer_url,
            application_url=application_url,
            localisation=localisation,
            publication_date=publication_date,
            end_publication_date=end_publication_date,
            beginning_date=beginning_date,
            education_level=education_level,
            experience=experience,
            diploma=diploma,
            languages=languages,
            specialisations=specialisations,
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

    _CONTRACT_KIND_MAPPING: dict[str, ContractKind] = {
        "CDI": ContractKind.CDI,
        "PERMANENT": ContractKind.PERMANENT,
        "VACATION": ContractKind.VACATION,
        "STAGE": ContractKind.STAGE,
    }

    def _map_contract_kind(
        self, contract_kind_str: Optional[str]
    ) -> Optional[ContractKind]:
        if not contract_kind_str:
            return None

        contract_kind_upper = contract_kind_str.upper()
        if contract_kind_upper.startswith("CDD"):
            return ContractKind.CDD

        return self._CONTRACT_KIND_MAPPING.get(contract_kind_upper)

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

    def _parse_optional_date(self, date_str: Optional[str]) -> Optional[datetime]:
        if not date_str:
            return None
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except (ValueError, TypeError, AttributeError):
            return None

    def _parse_beginning_date(self, date_str: Optional[str]) -> Optional[LimitDate]:
        if not date_str:
            return None

        try:
            parsed_date = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return LimitDate(value=parsed_date)
        except (ValueError, TypeError, AttributeError):
            return None

    def _map_experience(self, client_code: str) -> Optional[ExperienceLevel]:
        mapping: dict[str, Optional[ExperienceLevel]] = {
            "_TS_CO_ExperienceLevel_Nonrenseign": None,
            "debutant": ExperienceLevel.DEBUTANT,
            "confirme": ExperienceLevel.CONFIRME,
            "expert": ExperienceLevel.EXPERT,
        }
        return mapping[client_code]

    def _map_education_level(self, client_code: str) -> Optional[int]:
        mapping = {
            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8,
        }
        return mapping[client_code]

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
