import pytest

from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.departement_region import (
    chef_lieu_department_for_region,
    department_belongs_to_region,
    overseas_region_for_department,
    overseas_territory_for_country,
    region_et_zone_pour_departement,
    zone_pour_departement,
)
from referentiel.value_objects.department import Department
from referentiel.value_objects.region import Region


@pytest.mark.parametrize(
    ("department_code", "expected_region_code", "expected_area"),
    [
        pytest.param("01", "84", GeographicalArea.EUROPE, id="metropole"),
        pytest.param("2A", "94", GeographicalArea.EUROPE, id="corse"),
        pytest.param("971", "01", GeographicalArea.AMERIQUE, id="dom"),
    ],
)
def test_region_et_zone_pour_departement(
    department_code, expected_region_code, expected_area
):
    region_et_zone = region_et_zone_pour_departement(Department(code=department_code))

    assert region_et_zone is not None
    region, area = region_et_zone
    assert region.code == expected_region_code
    assert area == expected_area


def test_region_et_zone_pour_departement_inconnu():
    # Saint-Pierre-et-Miquelon: code de département valide, non couvert par
    # la table de correspondance région/zone.
    assert region_et_zone_pour_departement(Department(code="975")) is None


@pytest.mark.parametrize(
    ("department_code", "expected_area"),
    [
        pytest.param("01", GeographicalArea.EUROPE, id="metropole"),
        pytest.param("974", GeographicalArea.AFRIQUE, id="dom"),
        pytest.param("975", GeographicalArea.AMERIQUE, id="saint_pierre_et_miquelon"),
        pytest.param("977", GeographicalArea.AMERIQUE, id="saint_barthelemy"),
        pytest.param("978", GeographicalArea.AMERIQUE, id="saint_martin"),
        pytest.param("SPM", GeographicalArea.AMERIQUE, id="spm_code_alpha"),
        pytest.param("986", GeographicalArea.OCEANIE, id="wallis_et_futuna"),
        pytest.param("WLF", GeographicalArea.OCEANIE, id="wlf_code_alpha"),
        pytest.param("987", GeographicalArea.OCEANIE, id="polynesie"),
        pytest.param("988", GeographicalArea.OCEANIE, id="nouvelle_caledonie"),
    ],
)
def test_zone_pour_departement(department_code, expected_area):
    assert zone_pour_departement(Department(code=department_code)) == expected_area


@pytest.mark.parametrize(
    ("department_code", "region_code"),
    [
        pytest.param("13", "93", id="metropole"),
        pytest.param("2B", "94", id="corse"),
        pytest.param("971", "01", id="dom_region_insee"),
        pytest.param("976", "DOM", id="dom_region_generique"),
        pytest.param("975", "TOM", id="com"),
        pytest.param("WLF", "TOM", id="com_code_alpha"),
    ],
)
def test_department_belongs_to_region(department_code, region_code):
    assert department_belongs_to_region(
        Department(code=department_code), Region(code=region_code)
    )


@pytest.mark.parametrize(
    ("department_code", "region_code"),
    [
        pytest.param("13", "11", id="autre_region"),
        pytest.param("01", "01", id="code_departement_dans_region"),
        pytest.param("75", "DOM", id="metropole_region_dom"),
        pytest.param("971", "02", id="dom_autre_region"),
        pytest.param("971", "TOM", id="dom_region_tom"),
        pytest.param("988", "DOM", id="com_region_dom"),
        pytest.param("986", "04", id="com_region_insee"),
    ],
)
def test_department_does_not_belong_to_region(department_code, region_code):
    assert not department_belongs_to_region(
        Department(code=department_code), Region(code=region_code)
    )


@pytest.mark.parametrize(
    ("department_code", "region_code"),
    [
        ("971", "DOM"),
        ("972", "DOM"),
        ("973", "DOM"),
        ("974", "DOM"),
        ("976", "DOM"),
        ("975", "TOM"),
        ("977", "TOM"),
        ("978", "TOM"),
        ("986", "TOM"),
        ("987", "TOM"),
        ("988", "TOM"),
        ("SPM", "TOM"),
        ("WLF", "TOM"),
    ],
)
def test_overseas_region_for_department(department_code, region_code):
    region = overseas_region_for_department(Department(code=department_code))

    assert region == Region(code=region_code)


def test_overseas_region_for_metropolitan_department():
    assert overseas_region_for_department(Department(code="75")) is None


@pytest.mark.parametrize(
    ("country_code", "expected_department_code"),
    [("GLP", "971"), ("SPM", "975"), ("WLF", "WLF"), ("NCL", "988")],
)
def test_overseas_territory_for_country(country_code, expected_department_code):
    territory = overseas_territory_for_country(country_code)

    assert territory is not None
    assert territory.department == Department(code=expected_department_code)


@pytest.mark.parametrize("country_code", ["FRA", "DOM", "ATF", "DEU"])
def test_overseas_territory_for_country_returns_none(country_code):
    assert overseas_territory_for_country(country_code) is None


@pytest.mark.parametrize("region_code", sorted(Region.NAMES))
def test_chef_lieu_department_belongs_to_its_region(region_code):
    region = Region(code=region_code)

    department = chef_lieu_department_for_region(region)

    assert department is not None
    assert department_belongs_to_region(department, region)


@pytest.mark.parametrize(
    ("region_code", "expected_department_code"),
    [
        pytest.param("11", "75", id="ile_de_france"),
        pytest.param("24", "45", id="centre_val_de_loire"),
        pytest.param("27", "21", id="bourgogne_franche_comte"),
        pytest.param("28", "76", id="normandie"),
        pytest.param("32", "59", id="hauts_de_france"),
        pytest.param("44", "67", id="grand_est"),
        pytest.param("52", "44", id="pays_de_la_loire"),
        pytest.param("53", "35", id="bretagne"),
        pytest.param("75", "33", id="nouvelle_aquitaine"),
        pytest.param("76", "31", id="occitanie"),
        pytest.param("84", "69", id="auvergne_rhone_alpes"),
        pytest.param("93", "13", id="paca"),
        pytest.param("94", "2A", id="corse"),
        pytest.param("01", "971", id="guadeloupe"),
        pytest.param("02", "972", id="martinique"),
        pytest.param("03", "973", id="guyane"),
        pytest.param("04", "974", id="la_reunion"),
        pytest.param("06", "976", id="mayotte"),
    ],
)
def test_chef_lieu_department_for_region(region_code, expected_department_code):
    assert chef_lieu_department_for_region(Region(code=region_code)) == Department(
        code=expected_department_code
    )


@pytest.mark.parametrize("region_code", ["DOM", "TOM"])
def test_chef_lieu_department_for_overseas_grouping(region_code):
    assert chef_lieu_department_for_region(Region(code=region_code)) is None
