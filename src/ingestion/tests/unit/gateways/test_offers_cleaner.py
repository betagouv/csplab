from datetime import datetime, timezone

import pytest
from pydantic import ValidationError
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.language import Language
from referentiel.value_objects.language_level import LanguageLevel
from referentiel.value_objects.verse import Verse

from domain.entities.raw_offer import RawOffer
from infrastructure.external_gateways.dtos.talentsoft_dtos import TalentsoftLanguage
from infrastructure.gateways.offers_cleaner import OffersCleaner
from tests.factories.talentsoft_factories import (
    TalentsoftCodedObjectFactory,
    TalentsoftCustomCodeTableFactory,
    TalentsoftCustomFieldsFactory,
    TalentsoftDescriptionCustomFieldsFactory,
    TalentsoftDetailOfferFactory,
)

REFERENCE = "2024-OFFER-001"
SOURCE_ID = "11111111-2222-3333-4444-555555555555"


@pytest.fixture
def cleaner() -> OffersCleaner:
    return OffersCleaner()


def _make_raw_offer(reference: str = REFERENCE, **offer_kwargs) -> RawOffer:
    offer_dto = TalentsoftDetailOfferFactory.build(reference=reference, **offer_kwargs)
    return RawOffer(
        reference=reference,
        source_id=SOURCE_ID,
        data=offer_dto.model_dump(),
    )


def test_clean_returns_offer_with_correct_reference(cleaner):
    raw_offer = _make_raw_offer()

    offer = cleaner.clean(raw_offer)

    assert REFERENCE in offer.external_id


def test_clean_raises_when_no_data(cleaner):
    raw_offer = RawOffer(reference=REFERENCE, source_id=SOURCE_ID, data=None)

    with pytest.raises(ValueError, match="no data"):
        cleaner.clean(raw_offer)


def test_clean_raises_on_invalid_data(cleaner):
    raw_offer = RawOffer(
        reference=REFERENCE, source_id=SOURCE_ID, data={"invalid": "data"}
    )

    with pytest.raises(ValidationError):
        cleaner.clean(raw_offer)


@pytest.mark.parametrize(
    "salary_range_client_code, expected_verse",
    [
        ("Versant_FPT", Verse.FPT),
        ("Versant_FPH", Verse.FPH),
        ("Versant_FPE", Verse.FPE),
        (None, None),
    ],
)
def test_clean_maps_verse_from_salary_range(
    cleaner, salary_range_client_code, expected_verse
):
    salary_range = (
        TalentsoftCodedObjectFactory.build(clientCode=salary_range_client_code)
        if salary_range_client_code
        else None
    )
    raw_offer = _make_raw_offer(salaryRange=salary_range)

    offer = cleaner.clean(raw_offer)

    assert offer.verse == expected_verse


def test_clean_maps_verse_fph_from_aphp_reference(cleaner):
    raw_offer = _make_raw_offer(reference="APHP-2024-001")

    offer = cleaner.clean(raw_offer)

    assert offer.verse == Verse.FPH


@pytest.mark.parametrize(
    "category_code, expected_category",
    [
        ("CAT-AEF", Category.APLUS),
        ("CAT-ESD", Category.APLUS),
        ("CAT-ES", Category.APLUS),
        ("CAT-A", Category.A),
        ("CAT-B", Category.B),
        ("CAT-C", Category.C),
        ("UNKNOWN", None),
    ],
)
def test_clean_maps_category_from_custom_fields(
    cleaner, category_code, expected_category
):
    offer_dto_kwargs = {
        "customFields": TalentsoftCustomFieldsFactory.build(
            description=TalentsoftDescriptionCustomFieldsFactory.build(
                customCodeTable1=TalentsoftCustomCodeTableFactory.build(
                    clientCode=category_code
                )
            )
        )
    }
    raw_offer = _make_raw_offer(**offer_dto_kwargs)

    offer = cleaner.clean(raw_offer)

    assert offer.category == expected_category


@pytest.mark.parametrize(
    "area, country, region, department, "
    "expected_area, expected_region, expected_department",
    [
        (
            "_TS_CO_GeographicalArea_Europe",
            "FRA",
            "R24",
            "41",
            "EU",
            "24",
            "41",
        ),
        (
            "_TS_CO_GeographicalArea_Europe",
            "FRA",
            "R11",
            "75",
            "EU",
            "11",
            "75",
        ),
        (
            "_TS_CO_GeographicalArea_Afrique",
            "FRA",
            "_TS_CO_Region_DOM",
            "971",
            "AF",
            "DOM",
            "971",
        ),
        (
            "_TS_CO_GeographicalArea_AmriquesCaraibe",
            "FRA",
            "_TS_CO_Region_TOM",
            "987",
            "AM",
            "TOM",
            "987",
        ),
        (
            "_TS_CO_GeographicalArea_Ocanie",
            "FRA",
            "R84",
            "_TS_CO_Department_NouvelleCaldonie988",
            "OC",
            "84",
            "988",
        ),
    ],
)
def test_clean_maps_geographical_area(
    cleaner,
    area,
    country,
    region,
    department,
    expected_area,
    expected_region,
    expected_department,
):
    raw_offer = _make_raw_offer(
        geographicalLocation=[
            TalentsoftCodedObjectFactory.build(
                clientCode=area, type="offerGeographicalLocation"
            )
        ],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode=country, type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(clientCode=region, type="offerRegion")
        ],
        department=[
            TalentsoftCodedObjectFactory.build(
                clientCode=department, type="offerDepartment"
            )
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.area.value == expected_area
    assert offer.localisation.region.code == expected_region
    assert offer.localisation.department.code == expected_department


def test_clean_returns_none_localisation_when_area_missing(cleaner):
    raw_offer = _make_raw_offer(
        geographicalLocation=[],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(clientCode="R24", type="offerRegion")
        ],
        department=[
            TalentsoftCodedObjectFactory.build(clientCode="41", type="offerDepartment")
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is None


def test_clean_maps_title_and_organization(cleaner):
    offer_dto = TalentsoftDetailOfferFactory.build(
        reference=REFERENCE,
        title="INGÉNIEUR LOGICIEL",
        organisationName="Mairie de Paris",
    )
    raw_offer = RawOffer(
        reference=REFERENCE, source_id=SOURCE_ID, data=offer_dto.model_dump()
    )

    offer = cleaner.clean(raw_offer)

    assert offer.title == "INGÉNIEUR LOGICIEL"
    assert offer.organization == "Mairie de Paris"


def test_clean_external_id_uses_salary_range_client_code_as_prefix(cleaner):
    salary_range = TalentsoftCodedObjectFactory.build(clientCode="Versant_FPT")
    raw_offer = _make_raw_offer(reference=REFERENCE, salaryRange=salary_range)

    offer = cleaner.clean(raw_offer)

    assert offer.external_id == f"Versant_FPT-{REFERENCE}"


@pytest.mark.parametrize(
    "contract_code, expected",
    [
        ("TITULAIRE_CODE", ContractType.TITULAIRE_CONTRACTUEL),
        ("CONTRACTUEL_CDD", ContractType.CONTRACTUELS),
        ("TERRITORIAL_TIT", ContractType.TERRITORIAL),
        ("UNKNOWN_TYPE", None),
        (None, None),
    ],
)
def test_clean_maps_contract_type(cleaner, contract_code, expected):

    contract_type = (
        TalentsoftCodedObjectFactory.build(clientCode=contract_code)
        if contract_code
        else None
    )
    raw_offer = _make_raw_offer(contractType=contract_type)

    offer = cleaner.clean(raw_offer)

    assert offer.contract_type == expected


def test_clean_returns_none_url_on_invalid_offer_url(cleaner):
    raw_offer = _make_raw_offer(offerUrl="not-a-valid-url")

    offer = cleaner.clean(raw_offer)

    assert offer.offer_url is None


def test_clean_maps_application_url(cleaner):
    raw_offer = _make_raw_offer(applicationUrl="https://apply.example.com/job/123")

    offer = cleaner.clean(raw_offer)

    assert str(offer.application_url) == "https://apply.example.com/job/123"


def test_clean_returns_none_application_url_when_absent(cleaner):
    raw_offer = _make_raw_offer(applicationUrl=None)

    offer = cleaner.clean(raw_offer)

    assert offer.application_url is None


def test_clean_returns_none_beginning_date_on_invalid_format(cleaner):
    raw_offer = _make_raw_offer(beginningDate="not-a-date")

    offer = cleaner.clean(raw_offer)

    assert offer.beginning_date is None


def test_clean_returns_none_beginning_date_when_absent(cleaner):
    raw_offer = _make_raw_offer(beginningDate=None)

    offer = cleaner.clean(raw_offer)

    assert offer.beginning_date is None


def test_clean_maps_end_publication_date(cleaner):
    raw_offer = _make_raw_offer(endPublicationDate="2025-06-30T00:00:00Z")

    offer = cleaner.clean(raw_offer)

    assert offer.end_publication_date == datetime(2025, 6, 30, tzinfo=timezone.utc)


def test_clean_returns_none_end_publication_date_when_absent(cleaner):
    raw_offer = _make_raw_offer(endPublicationDate=None)

    offer = cleaner.clean(raw_offer)

    assert offer.end_publication_date is None


@pytest.mark.parametrize(
    "client_code, expected",
    [
        ("A", 1),
        ("B", 2),
        ("C", 3),
        ("D", 4),
        ("E", 5),
        ("F", 6),
        ("G", 7),
        ("H", 8),
    ],
)
def test_clean_maps_education_level(cleaner, client_code, expected):
    education = TalentsoftCodedObjectFactory.build(clientCode=client_code)
    raw_offer = _make_raw_offer(educationLevel=education)

    offer = cleaner.clean(raw_offer)

    assert offer.education_level == expected


def test_clean_returns_none_education_level_when_absent(cleaner):
    raw_offer = _make_raw_offer(educationLevel=None)

    offer = cleaner.clean(raw_offer)

    assert offer.education_level is None


@pytest.mark.parametrize(
    "client_code, expected",
    [
        ("_TS_CO_ExperienceLevel_Nonrenseign", None),
        ("debutant", ExperienceLevel.DEBUTANT),
        ("confirme", ExperienceLevel.CONFIRME),
        ("expert", ExperienceLevel.EXPERT),
    ],
)
def test_clean_maps_experience(cleaner, client_code, expected):
    experience = TalentsoftCodedObjectFactory.build(clientCode=client_code)
    raw_offer = _make_raw_offer(experienceLevel=experience)

    offer = cleaner.clean(raw_offer)

    assert offer.experience == expected


def test_clean_returns_none_experience_when_absent(cleaner):
    raw_offer = _make_raw_offer(experienceLevel=None)

    offer = cleaner.clean(raw_offer)

    assert offer.experience is None


def test_clean_maps_specialisations(cleaner):
    raw_offer = _make_raw_offer(
        specialisations=[
            TalentsoftCodedObjectFactory.build(clientCode="SPEC_A"),
            TalentsoftCodedObjectFactory.build(clientCode="SPEC_B"),
        ]
    )

    offer = cleaner.clean(raw_offer)

    assert offer.specialisations == ["SPEC_A", "SPEC_B"]


def test_clean_returns_empty_specialisations_when_absent(cleaner):
    raw_offer = _make_raw_offer(specialisations=[])

    offer = cleaner.clean(raw_offer)

    assert offer.specialisations == []


def test_clean_maps_diploma(cleaner):
    diploma = TalentsoftCodedObjectFactory.build(clientCode="LICENCE")
    raw_offer = _make_raw_offer(diploma=diploma)

    offer = cleaner.clean(raw_offer)

    assert offer.diploma == "LICENCE"


def test_clean_returns_none_diploma_when_absent(cleaner):
    raw_offer = _make_raw_offer(diploma=None)

    offer = cleaner.clean(raw_offer)

    assert offer.diploma is None


def test_clean_maps_languages(cleaner):
    raw_offer = _make_raw_offer(
        languages=[
            TalentsoftLanguage(
                languageName=TalentsoftCodedObjectFactory.build(clientCode="EN"),
                languageLevel=TalentsoftCodedObjectFactory.build(clientCode="B2"),
            )
        ]
    )

    offer = cleaner.clean(raw_offer)

    assert offer.languages == [Language(iso_code="EN", language_level=LanguageLevel.B2)]


def test_clean_returns_empty_languages_when_absent(cleaner):
    raw_offer = _make_raw_offer(languages=[])

    offer = cleaner.clean(raw_offer)

    assert offer.languages == []


def test_clean_maps_raw_region_code_without_prefix(cleaner):
    raw_offer = _make_raw_offer(
        geographicalLocation=[
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_GeographicalArea_Europe",
                type="offerGeographicalLocation",
            )
        ],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(clientCode="11", type="offerRegion")
        ],
        department=[
            TalentsoftCodedObjectFactory.build(clientCode="75", type="offerDepartment")
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is not None
    assert offer.localisation.region.code == "11"


def test_clean_returns_none_localisation_on_invalid_region_code(cleaner):
    raw_offer = _make_raw_offer(
        geographicalLocation=[
            TalentsoftCodedObjectFactory.build(
                clientCode="_TS_CO_GeographicalArea_Europe",
                type="offerGeographicalLocation",
            )
        ],
        country=[
            TalentsoftCodedObjectFactory.build(clientCode="FRA", type="offerCountry")
        ],
        region=[
            TalentsoftCodedObjectFactory.build(
                clientCode="INVALID_REGION", type="offerRegion"
            )
        ],
        department=[
            TalentsoftCodedObjectFactory.build(clientCode="75", type="offerDepartment")
        ],
    )

    offer = cleaner.clean(raw_offer)

    assert offer.localisation is None
