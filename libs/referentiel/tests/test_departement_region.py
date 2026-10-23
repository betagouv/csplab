import pytest

from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.departement_region import (
    department_belongs_to_region,
    overseas_region_for_department,
    region_et_zone_pour_departement,
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
