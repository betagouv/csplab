"""Integration tests for CleanRawOfferUseCase wired with the real OffersCleaner."""

import datetime

import pytest

from application.use_cases.clean_raw_offer import CleanRawOfferUseCase
from domain.entities.offer import Offer
from domain.entities.raw_offer import RawOffer
from domain.value_objects.category import Category
from domain.value_objects.contract_type import ContractType
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.verse import Verse
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
def use_case() -> CleanRawOfferUseCase:
    return CleanRawOfferUseCase(offers_cleaner=OffersCleaner())


def _raw_offer(**kwargs) -> RawOffer:
    offer_dto = TalentsoftDetailOfferFactory.build(reference=REFERENCE, **kwargs)
    return RawOffer(
        reference=REFERENCE,
        source_id=SOURCE_ID,
        data=offer_dto.model_dump(),
    )


def test_execute_returns_offer_with_reference_and_source_id(use_case):
    result = use_case.execute(_raw_offer())

    assert isinstance(result, Offer)
    assert result.reference == REFERENCE
    assert result.source_id == SOURCE_ID


def test_execute_maps_title_and_organization(use_case):
    raw = _raw_offer(title="DIRECTEUR GÉNÉRAL", organisationName="Mairie de Lyon")

    result = use_case.execute(raw)

    assert result.title == "DIRECTEUR GÉNÉRAL"
    assert result.organization == "Mairie de Lyon"


@pytest.mark.parametrize(
    "salary_range_code, expected_verse",
    [
        ("Versant_FPT", Verse.FPT),
        ("Versant_FPH", Verse.FPH),
        ("Versant_FPE", Verse.FPE),
    ],
)
def test_execute_maps_verse(use_case, salary_range_code, expected_verse):
    salary_range = TalentsoftCodedObjectFactory.build(clientCode=salary_range_code)
    result = use_case.execute(_raw_offer(salaryRange=salary_range))

    assert result.verse == expected_verse


@pytest.mark.parametrize(
    "contract_code, expected",
    [
        ("TITULAIRE_CDI", ContractType.TITULAIRE_CONTRACTUEL),
        ("CONTRACTUEL_CDD", ContractType.CONTRACTUELS),
        ("TERRITORIAL_TIT", ContractType.TERRITORIAL),
        ("INCONNU", None),
        (None, None),
    ],
)
def test_execute_maps_contract_type(use_case, contract_code, expected):
    contract_type = (
        TalentsoftCodedObjectFactory.build(clientCode=contract_code)
        if contract_code
        else None
    )
    result = use_case.execute(_raw_offer(contractType=contract_type))

    assert result.contract_type == expected


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
def test_execute_maps_category(use_case, category_code, expected_category):
    raw = _raw_offer(
        customFields=TalentsoftCustomFieldsFactory.build(
            description=TalentsoftDescriptionCustomFieldsFactory.build(
                customCodeTable1=TalentsoftCustomCodeTableFactory.build(
                    clientCode=category_code
                )
            )
        )
    )

    result = use_case.execute(raw)

    assert result.category == expected_category


def test_execute_maps_localisation(use_case):
    raw = _raw_offer(
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
            TalentsoftCodedObjectFactory.build(clientCode="R11", type="offerRegion")
        ],
        department=[
            TalentsoftCodedObjectFactory.build(clientCode="75", type="offerDepartment")
        ],
    )

    result = use_case.execute(raw)

    assert result.localisation is not None
    assert result.localisation.area.value == "EU"
    assert str(result.localisation.country) == "FRA"
    assert result.localisation.region.code == "11"
    assert result.localisation.department.code == "75"


def test_execute_returns_none_localisation_when_missing(use_case):
    raw = _raw_offer(geographicalLocation=[], country=[], region=[], department=[])

    result = use_case.execute(raw)

    assert result.localisation is None


def test_execute_raises_when_raw_offer_has_no_data(use_case):
    raw = RawOffer(reference=REFERENCE, source_id=SOURCE_ID, data=None)

    with pytest.raises(ValueError, match="no data"):
        use_case.execute(raw)


def test_execute_external_id_uses_salary_range_client_code_as_prefix(use_case):
    salary_range = TalentsoftCodedObjectFactory.build(clientCode="Versant_FPT")
    result = use_case.execute(_raw_offer(salaryRange=salary_range))

    assert result.external_id == f"Versant_FPT-{REFERENCE}"


def test_execute_sets_beginning_date_when_present(use_case):
    raw = _raw_offer(beginningDate="2025-09-01T00:00:00Z")

    result = use_case.execute(raw)

    assert result.beginning_date == LimitDate(
        value=datetime.datetime(2025, 9, 1, 0, 0, tzinfo=datetime.timezone.utc)
    )


def test_execute_sets_none_beginning_date_when_absent(use_case):
    raw = _raw_offer(beginningDate=None)

    result = use_case.execute(raw)

    assert result.beginning_date is None
