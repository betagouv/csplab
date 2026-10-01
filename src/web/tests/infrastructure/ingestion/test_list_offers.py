from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.offer_criteria import OfferCriteria
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


@pytest.fixture(name="offers")
def offers_fixture(db):
    return {
        "archived_expected": OfferDjangoFactory(
            reference="test-expected-archived", archived_at=datetime.now(UTC)
        ),
        "archived_other": OfferDjangoFactory(
            reference="test-other-archived", archived_at=datetime.now(UTC)
        ),
        "active_expected": OfferDjangoFactory(reference="test-expected-active"),
        "active_other": OfferDjangoFactory(reference="test-other-active"),
    }


@pytest.mark.parametrize(
    "active, expected_keys",
    [
        pytest.param(True, ["active_expected", "active_other"], id="active_offers"),
        pytest.param(
            False, ["archived_expected", "archived_other"], id="archived_offers"
        ),
    ],
)
def test_list_offers_result(ingestion_container, offers, active, expected_keys):
    input_data = GetFilteredOffersInput(active=active)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers[key].reference for key in expected_keys
    }


@pytest.mark.parametrize(
    "offset,limit,expected_keys",
    [
        pytest.param(0, 1, ["active_other"], id="sliced"),
        pytest.param(0, 2, ["active_expected", "active_other"], id="sliced_all"),
        pytest.param(10, 10, [], id="sliced_out_of_bounds"),
    ],
)
def test_list_offers_page_slice(
    ingestion_container, offers, offset, limit, expected_keys
):
    input_data = GetFilteredOffersInput(active=True)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert result.count() == len(["active_expected", "active_other"])

    sliced = list(result.slice(offset=offset, limit=limit))
    assert {offer.reference for offer in sliced} == {
        offers[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_category")
def offers_by_category_fixture(db):
    return {
        "cat_a": OfferDjangoFactory(reference="test-cat-a", category=Category.A),
        "cat_b": OfferDjangoFactory(reference="test-cat-b", category=Category.B),
        "cat_c": OfferDjangoFactory(reference="test-cat-c", category=Category.C),
    }


@pytest.mark.parametrize(
    "category, expected_keys",
    [
        pytest.param(None, ["cat_a", "cat_b", "cat_c"], id="no_filter"),
        pytest.param([Category.A], ["cat_a"], id="single_category"),
        pytest.param(
            [Category.A, Category.B], ["cat_a", "cat_b"], id="multiple_categories"
        ),
        pytest.param([Category.HORS_CATEGORIE], [], id="unmatched_category"),
    ],
)
def test_list_offers_filtered_by_category(
    ingestion_container, offers_by_category, category, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, category=category)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_category[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_verse")
def offers_by_verse_fixture(db):
    return {
        "fpe": OfferDjangoFactory(reference="test-fpe", verse=Verse.FPE),
        "fpt": OfferDjangoFactory(reference="test-fpt", verse=Verse.FPT),
        "fph": OfferDjangoFactory(reference="test-fph", verse=Verse.FPH),
    }


@pytest.mark.parametrize(
    "verse, expected_keys",
    [
        pytest.param(None, ["fpe", "fpt", "fph"], id="no_filter"),
        pytest.param([Verse.FPE], ["fpe"], id="single_verse"),
        pytest.param([Verse.FPE, Verse.FPT], ["fpe", "fpt"], id="multiple_verses"),
    ],
)
def test_list_offers_filtered_by_verse(
    ingestion_container, offers_by_verse, verse, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, verse=verse)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_verse[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_contract_type")
def offers_by_contract_type_fixture(db):
    return {
        "contractuels": OfferDjangoFactory(
            reference="test-contractuels", contract_type=ContractType.CONTRACTUELS
        ),
        "territorial": OfferDjangoFactory(
            reference="test-territorial", contract_type=ContractType.TERRITORIAL
        ),
        "titulaire": OfferDjangoFactory(
            reference="test-titulaire",
            contract_type=ContractType.TITULAIRE_CONTRACTUEL,
        ),
    }


@pytest.mark.parametrize(
    "contract_type, expected_keys",
    [
        pytest.param(
            None,
            ["contractuels", "territorial", "titulaire"],
            id="no_filter",
        ),
        pytest.param(
            [ContractType.CONTRACTUELS], ["contractuels"], id="single_contract_type"
        ),
        pytest.param(
            [ContractType.CONTRACTUELS, ContractType.TERRITORIAL],
            ["contractuels", "territorial"],
            id="multiple_contract_types",
        ),
    ],
)
def test_list_offers_filtered_by_contract_type(
    ingestion_container, offers_by_contract_type, contract_type, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, contract_type=contract_type)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_contract_type[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_experience_level")
def offers_by_experience_level_fixture(db):
    return {
        "debutant": OfferDjangoFactory(
            reference="test-debutant",
            criteria=OfferCriteria(experience_level=ExperienceLevel.DEBUTANT).to_dict(),
        ),
        "confirme": OfferDjangoFactory(
            reference="test-confirme",
            criteria=OfferCriteria(experience_level=ExperienceLevel.CONFIRME).to_dict(),
        ),
        "expert": OfferDjangoFactory(
            reference="test-expert",
            criteria=OfferCriteria(experience_level=ExperienceLevel.EXPERT).to_dict(),
        ),
    }


@pytest.mark.parametrize(
    "experience_level, expected_keys",
    [
        pytest.param(None, ["debutant", "confirme", "expert"], id="no_filter"),
        pytest.param(
            [ExperienceLevel.DEBUTANT], ["debutant"], id="single_experience_level"
        ),
        pytest.param(
            [ExperienceLevel.DEBUTANT, ExperienceLevel.EXPERT],
            ["debutant", "expert"],
            id="multiple_experience_levels",
        ),
    ],
)
def test_list_offers_filtered_by_experience_level(
    ingestion_container, offers_by_experience_level, experience_level, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, experience_level=experience_level)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_experience_level[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_management")
def offers_by_management_fixture(db):
    return {
        "sans": OfferDjangoFactory(
            reference="test-sans",
            conditions={"management": Management.SANS.name},
        ),
        "avec": OfferDjangoFactory(
            reference="test-avec",
            conditions={"management": Management.AVEC.name},
        ),
    }


@pytest.mark.parametrize(
    "management, expected_keys",
    [
        pytest.param(None, ["sans", "avec"], id="no_filter"),
        pytest.param([Management.SANS], ["sans"], id="single_management"),
        pytest.param(
            [Management.SANS, Management.AVEC],
            ["sans", "avec"],
            id="multiple_managements",
        ),
    ],
)
def test_list_offers_filtered_by_management(
    ingestion_container, offers_by_management, management, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, management=management)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_management[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_working_place")
def offers_by_working_place_fixture(db):
    return {
        "sur_site": OfferDjangoFactory(
            reference="test-sur-site",
            conditions={"lieu_de_travail": WorkingPlace.SUR_SITE.name},
        ),
        "teletravail": OfferDjangoFactory(
            reference="test-teletravail",
            conditions={"lieu_de_travail": WorkingPlace.TELETRAVAIL.name},
        ),
    }


@pytest.mark.parametrize(
    "working_place, expected_keys",
    [
        pytest.param(None, ["sur_site", "teletravail"], id="no_filter"),
        pytest.param([WorkingPlace.SUR_SITE], ["sur_site"], id="single_working_place"),
        pytest.param(
            [WorkingPlace.SUR_SITE, WorkingPlace.TELETRAVAIL],
            ["sur_site", "teletravail"],
            id="multiple_working_places",
        ),
    ],
)
def test_list_offers_filtered_by_working_place(
    ingestion_container, offers_by_working_place, working_place, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, working_place=working_place)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_working_place[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_region")
def offers_by_region_fixture(db):
    return {
        "idf": OfferDjangoFactory(
            reference="test-idf",
            country="FRA",
            region="11",
            department="75",
        ),
        "ara": OfferDjangoFactory(
            reference="test-ara",
            country="FRA",
            region="84",
            department="69",
        ),
    }


@pytest.mark.parametrize(
    "region, expected_keys",
    [
        pytest.param(None, ["idf", "ara"], id="no_filter"),
        pytest.param([Region(code="11")], ["idf"], id="single_region"),
        pytest.param(
            [Region(code="11"), Region(code="84")],
            ["idf", "ara"],
            id="multiple_regions",
        ),
    ],
)
def test_list_offers_filtered_by_region(
    ingestion_container, offers_by_region, region, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, region=region)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_region[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_department")
def offers_by_department_fixture(db):
    return {
        "paris": OfferDjangoFactory(
            reference="test-paris",
            country="FRA",
            region="11",
            department="75",
        ),
        "rhone": OfferDjangoFactory(
            reference="test-rhone",
            country="FRA",
            region="84",
            department="69",
        ),
    }


@pytest.mark.parametrize(
    "department, expected_keys",
    [
        pytest.param(None, ["paris", "rhone"], id="no_filter"),
        pytest.param([Department(code="75")], ["paris"], id="single_department"),
        pytest.param(
            [Department(code="75"), Department(code="69")],
            ["paris", "rhone"],
            id="multiple_departments",
        ),
    ],
)
def test_list_offers_filtered_by_department(
    ingestion_container, offers_by_department, department, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, department=department)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_department[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_country")
def offers_by_country_fixture(db):
    return {
        "france": OfferDjangoFactory(
            reference="test-france",
            country="FRA",
            region="11",
            department="75",
        ),
        "belgium": OfferDjangoFactory(
            reference="test-belgium",
            country="BEL",
            region="11",
            department="75",
        ),
    }


@pytest.mark.parametrize(
    "country, expected_keys",
    [
        pytest.param(None, ["france", "belgium"], id="no_filter"),
        pytest.param([Country("FRA")], ["france"], id="single_country"),
        pytest.param(
            [Country("FRA"), Country("BEL")],
            ["france", "belgium"],
            id="multiple_countries",
        ),
    ],
)
def test_list_offers_filtered_by_country(
    ingestion_container, offers_by_country, country, expected_keys
):
    input_data = GetFilteredOffersInput(active=True, country=country)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_country[key].reference for key in expected_keys
    }


@pytest.fixture(name="offers_by_multiple_criteria")
def offers_by_multiple_criteria_fixture(db):
    return {
        "match": OfferDjangoFactory(
            reference="test-match",
            category=Category.A,
            verse=Verse.FPE,
            contract_type=ContractType.CONTRACTUELS,
            criteria=OfferCriteria(experience_level=ExperienceLevel.DEBUTANT).to_dict(),
        ),
        "match_other_values": OfferDjangoFactory(
            reference="test-match-other-values",
            category=Category.B,
            verse=Verse.FPT,
            contract_type=ContractType.CONTRACTUELS,
            criteria=OfferCriteria(experience_level=ExperienceLevel.EXPERT).to_dict(),
        ),
        "wrong_category": OfferDjangoFactory(
            reference="test-wrong-category",
            category=Category.C,
            verse=Verse.FPE,
            contract_type=ContractType.CONTRACTUELS,
            criteria=OfferCriteria(experience_level=ExperienceLevel.DEBUTANT).to_dict(),
        ),
        "wrong_contract_type": OfferDjangoFactory(
            reference="test-wrong-contract-type",
            category=Category.A,
            verse=Verse.FPE,
            contract_type=ContractType.TERRITORIAL,
            criteria=OfferCriteria(experience_level=ExperienceLevel.DEBUTANT).to_dict(),
        ),
        "wrong_experience_level": OfferDjangoFactory(
            reference="test-wrong-experience-level",
            category=Category.A,
            verse=Verse.FPE,
            contract_type=ContractType.CONTRACTUELS,
            criteria=OfferCriteria(experience_level=ExperienceLevel.CONFIRME).to_dict(),
        ),
    }


def test_list_offers_filtered_by_multiple_criteria(
    ingestion_container, offers_by_multiple_criteria
):
    input_data = GetFilteredOffersInput(
        active=True,
        category=[Category.A, Category.B],
        verse=[Verse.FPE, Verse.FPT],
        contract_type=[ContractType.CONTRACTUELS],
        experience_level=[ExperienceLevel.DEBUTANT, ExperienceLevel.EXPERT],
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_multiple_criteria[key].reference
        for key in ["match", "match_other_values"]
    }


@pytest.fixture(name="offers_by_geo")
def offers_by_geo_fixture(db):
    return {
        "paris": OfferDjangoFactory(
            reference="test-paris-geo",
            country="FRA",
            region="11",
            department="75",
            latitude=48.8566,
            longitude=2.3522,
        ),
        "lyon": OfferDjangoFactory(
            reference="test-lyon-geo",
            country="FRA",
            region="84",
            department="69",
            latitude=45.7640,
            longitude=4.8357,
        ),
        "no_coordinates": OfferDjangoFactory(
            reference="test-no-coordinates-geo",
            country="FRA",
            region="11",
            department="75",
        ),
    }


@pytest.mark.parametrize(
    "latitude,longitude,radius_km,expected_keys",
    [
        pytest.param(
            None, None, None, ["paris", "lyon", "no_coordinates"], id="no_filter"
        ),
        pytest.param(48.8566, 2.3522, 50, ["paris"], id="small_radius_around_paris"),
        pytest.param(
            48.8566, 2.3522, 500, ["paris", "lyon"], id="wide_radius_around_paris"
        ),
    ],
)
def test_list_offers_filtered_by_geo(
    ingestion_container, offers_by_geo, latitude, longitude, radius_km, expected_keys
):
    input_data = GetFilteredOffersInput(
        active=True,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.reference for offer in result._qs} == {
        offers_by_geo[key].reference for key in expected_keys
    }


def test_get_filtered_raises_error(db, ingestion_container):
    shared_container = ingestion_container.shared_container()
    offers_repo = shared_container.offers_repository()

    offers_repo.get_filtered = MagicMock(side_effect=Exception("db error"))

    with pytest.raises(Exception, match="db error"):
        input_data = GetFilteredOffersInput(active=True)
        ingestion_container.list_offers_usecase().execute(input_data=input_data)
