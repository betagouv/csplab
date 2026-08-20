import pytest

from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.departement_region import (
    region_et_zone_pour_departement,
)
from referentiel.value_objects.department import Department


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
