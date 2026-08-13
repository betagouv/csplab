from datetime import datetime
from unittest.mock import MagicMock

import pytest
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.category import Category
from referentiel.value_objects.contract_type import ContractType
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.experience_level import ExperienceLevel
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.offer_conditions import Management, WorkingPlace
from referentiel.value_objects.offer_criteria import OfferCriteria
from referentiel.value_objects.region import Region
from referentiel.value_objects.verse import Verse

from application.ingestion.interfaces.list_offers_input import GetFilteredOffersInput
from infrastructure.factories.referentiel.offer_factory import OfferFactory


@pytest.fixture(name="offers")
def offers_fixture(db):
    return {
        "archived_expected": OfferFactory.create_model(
            external_id="test-expected-archived", archived_at=datetime.now()
        ),
        "archived_other": OfferFactory.create_model(
            external_id="test-other-archived", archived_at=datetime.now()
        ),
        "active_expected": OfferFactory.create_model(
            external_id="test-expected-active"
        ),
        "active_other": OfferFactory.create_model(external_id="test-other-active"),
    }


@pytest.mark.parametrize(
    "active, external_id_contains, expected_keys",
    [
        pytest.param(True, "unknown", [], id="empty_result"),
        pytest.param(
            True, None, ["active_expected", "active_other"], id="all_active_offers"
        ),
        pytest.param(
            True,
            "expected",
            ["active_expected"],
            id="active_offers_containing_expected",
        ),
        pytest.param(
            False,
            None,
            ["archived_expected", "archived_other"],
            id="all_archived_offers",
        ),
        pytest.param(
            False,
            "expected",
            ["archived_expected"],
            id="archived_offers_containing_expected",
        ),
    ],
)
def test_list_offers_result(
    ingestion_container, offers, active, external_id_contains, expected_keys
):
    input_data = GetFilteredOffersInput(
        active=active, external_id_contains=external_id_contains
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers[key].external_id for key in expected_keys
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
    input_data = GetFilteredOffersInput(active=True, external_id_contains=None)
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert result.count() == len(["active_expected", "active_other"])

    sliced = list(result.slice(offset=offset, limit=limit))
    assert {offer.external_id for offer in sliced} == {
        offers[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_category")
def offers_by_category_fixture(db):
    return {
        "cat_a": OfferFactory.create_model(
            external_id="test-cat-a", category=Category.A
        ),
        "cat_b": OfferFactory.create_model(
            external_id="test-cat-b", category=Category.B
        ),
        "cat_c": OfferFactory.create_model(
            external_id="test-cat-c", category=Category.C
        ),
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
    input_data = GetFilteredOffersInput(
        active=True, external_id_contains=None, category=category
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_category[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_verse")
def offers_by_verse_fixture(db):
    return {
        "fpe": OfferFactory.create_model(external_id="test-fpe", verse=Verse.FPE),
        "fpt": OfferFactory.create_model(external_id="test-fpt", verse=Verse.FPT),
        "fph": OfferFactory.create_model(external_id="test-fph", verse=Verse.FPH),
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
    input_data = GetFilteredOffersInput(
        active=True, external_id_contains=None, verse=verse
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_verse[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_contract_type")
def offers_by_contract_type_fixture(db):
    return {
        "contractuels": OfferFactory.create_model(
            external_id="test-contractuels", contract_type=ContractType.CONTRACTUELS
        ),
        "territorial": OfferFactory.create_model(
            external_id="test-territorial", contract_type=ContractType.TERRITORIAL
        ),
        "titulaire": OfferFactory.create_model(
            external_id="test-titulaire",
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
    input_data = GetFilteredOffersInput(
        active=True, external_id_contains=None, contract_type=contract_type
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_contract_type[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_experience_level")
def offers_by_experience_level_fixture(db):
    return {
        "debutant": OfferFactory.create_model(
            external_id="test-debutant",
            criteria=OfferCriteria(experience_level=ExperienceLevel.DEBUTANT),
        ),
        "confirme": OfferFactory.create_model(
            external_id="test-confirme",
            criteria=OfferCriteria(experience_level=ExperienceLevel.CONFIRME),
        ),
        "expert": OfferFactory.create_model(
            external_id="test-expert",
            criteria=OfferCriteria(experience_level=ExperienceLevel.EXPERT),
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
    input_data = GetFilteredOffersInput(
        active=True, external_id_contains=None, experience_level=experience_level
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_experience_level[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_management")
def offers_by_management_fixture(db):
    return {
        "sans": OfferFactory.create_model(
            external_id="test-sans",
            conditions={"management": Management.SANS.name},
        ),
        "avec": OfferFactory.create_model(
            external_id="test-avec",
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
    input_data = GetFilteredOffersInput(
        active=True, external_id_contains=None, management=management
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_management[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_working_place")
def offers_by_working_place_fixture(db):
    return {
        "sur_site": OfferFactory.create_model(
            external_id="test-sur-site",
            conditions={"lieu_de_travail": WorkingPlace.SUR_SITE.name},
        ),
        "teletravail": OfferFactory.create_model(
            external_id="test-teletravail",
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
    input_data = GetFilteredOffersInput(
        active=True, external_id_contains=None, working_place=working_place
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_working_place[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_region")
def offers_by_region_fixture(db):
    return {
        "idf": OfferFactory.create_model(
            external_id="test-idf",
            localisation=Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="11"),
                department=Department(code="75"),
            ),
        ),
        "ara": OfferFactory.create_model(
            external_id="test-ara",
            localisation=Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="84"),
                department=Department(code="69"),
            ),
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
    input_data = GetFilteredOffersInput(
        active=True, external_id_contains=None, region=region
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_region[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_department")
def offers_by_department_fixture(db):
    return {
        "paris": OfferFactory.create_model(
            external_id="test-paris",
            localisation=Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="11"),
                department=Department(code="75"),
            ),
        ),
        "rhone": OfferFactory.create_model(
            external_id="test-rhone",
            localisation=Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="84"),
                department=Department(code="69"),
            ),
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
    input_data = GetFilteredOffersInput(
        active=True, external_id_contains=None, department=department
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_department[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_country")
def offers_by_country_fixture(db):
    return {
        "france": OfferFactory.create_model(
            external_id="test-france",
            localisation=Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="11"),
                department=Department(code="75"),
            ),
        ),
        "belgium": OfferFactory.create_model(
            external_id="test-belgium",
            localisation=Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("BEL"),
                region=Region(code="11"),
                department=Department(code="75"),
            ),
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
    input_data = GetFilteredOffersInput(
        active=True, external_id_contains=None, country=country
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_country[key].external_id for key in expected_keys
    }


@pytest.fixture(name="offers_by_multiple_criteria")
def offers_by_multiple_criteria_fixture(db):
    return {
        "match": OfferFactory.create_model(
            external_id="test-match",
            category=Category.A,
            verse=Verse.FPE,
            contract_type=ContractType.CONTRACTUELS,
            criteria=OfferCriteria(experience_level=ExperienceLevel.DEBUTANT),
        ),
        "match_other_values": OfferFactory.create_model(
            external_id="test-match-other-values",
            category=Category.B,
            verse=Verse.FPT,
            contract_type=ContractType.CONTRACTUELS,
            criteria=OfferCriteria(experience_level=ExperienceLevel.EXPERT),
        ),
        "wrong_category": OfferFactory.create_model(
            external_id="test-wrong-category",
            category=Category.C,
            verse=Verse.FPE,
            contract_type=ContractType.CONTRACTUELS,
            criteria=OfferCriteria(experience_level=ExperienceLevel.DEBUTANT),
        ),
        "wrong_contract_type": OfferFactory.create_model(
            external_id="test-wrong-contract-type",
            category=Category.A,
            verse=Verse.FPE,
            contract_type=ContractType.TERRITORIAL,
            criteria=OfferCriteria(experience_level=ExperienceLevel.DEBUTANT),
        ),
        "wrong_experience_level": OfferFactory.create_model(
            external_id="test-wrong-experience-level",
            category=Category.A,
            verse=Verse.FPE,
            contract_type=ContractType.CONTRACTUELS,
            criteria=OfferCriteria(experience_level=ExperienceLevel.CONFIRME),
        ),
    }


def test_list_offers_filtered_by_multiple_criteria(
    ingestion_container, offers_by_multiple_criteria
):
    input_data = GetFilteredOffersInput(
        active=True,
        external_id_contains=None,
        category=[Category.A, Category.B],
        verse=[Verse.FPE, Verse.FPT],
        contract_type=[ContractType.CONTRACTUELS],
        experience_level=[ExperienceLevel.DEBUTANT, ExperienceLevel.EXPERT],
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_multiple_criteria[key].external_id
        for key in ["match", "match_other_values"]
    }


@pytest.fixture(name="offers_by_geo")
def offers_by_geo_fixture(db):
    return {
        "paris": OfferFactory.create_model(
            external_id="test-paris-geo",
            localisation=Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="11"),
                department=Department(code="75"),
                latitude=48.8566,
                longitude=2.3522,
            ),
        ),
        "lyon": OfferFactory.create_model(
            external_id="test-lyon-geo",
            localisation=Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="84"),
                department=Department(code="69"),
                latitude=45.7640,
                longitude=4.8357,
            ),
        ),
        "no_coordinates": OfferFactory.create_model(
            external_id="test-no-coordinates-geo",
            localisation=Localisation(
                area=GeographicalArea.EUROPE,
                country=Country("FRA"),
                region=Region(code="11"),
                department=Department(code="75"),
            ),
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
        external_id_contains=None,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
    )
    result = ingestion_container.list_offers_usecase().execute(input_data=input_data)

    assert {offer.external_id for offer in result._qs} == {
        offers_by_geo[key].external_id for key in expected_keys
    }


def test_get_filtered_raises_error(db, ingestion_container):
    shared_container = ingestion_container.shared_container()
    offers_repo = shared_container.offers_repository()

    offers_repo.get_filtered = MagicMock(side_effect=Exception("db error"))

    with pytest.raises(Exception, match="db error"):
        input_data = GetFilteredOffersInput(active=True, external_id_contains=None)
        ingestion_container.list_offers_usecase().execute(input_data=input_data)
