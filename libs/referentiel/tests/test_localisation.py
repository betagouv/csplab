import pytest

from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region


def test_from_department_builds_localisation():
    localisation = Localisation.from_department(
        Department(code="01"), latitude=45.7, longitude=5.0
    )

    assert localisation is not None
    assert localisation.area == GeographicalArea.EUROPE
    assert localisation.region.code == "84"
    assert str(localisation.country) == "FRA"
    assert localisation.department.code == "01"
    assert localisation.latitude == 45.7
    assert localisation.longitude == 5.0


def test_from_department_unmapped_returns_none():
    assert Localisation.from_department(Department(code="975")) is None


def test_localisation_abroad_has_no_region_nor_department():
    localisation = Localisation(
        area=GeographicalArea.EUROPE,
        country=Country("DEU"),
        region=None,
        department=None,
        label="Berlin",
    )

    assert not localisation.is_in_france
    assert str(localisation) == localisation.country.short_name


@pytest.mark.parametrize(
    ("region", "department"),
    [
        pytest.param(None, None, id="sans_region_ni_departement"),
        pytest.param(Region(code="11"), None, id="sans_departement"),
        pytest.param(None, Department(code="75"), id="sans_region"),
    ],
)
def test_localisation_in_france_requires_region_and_department(region, department):
    with pytest.raises(ValueError, match="in France"):
        Localisation(
            area=GeographicalArea.EUROPE,
            country=Country("FRA"),
            region=region,
            department=department,
        )


@pytest.mark.parametrize(
    ("region", "department"),
    [
        pytest.param(Region(code="11"), Department(code="75"), id="complete"),
        pytest.param(Region(code="11"), None, id="region_seule"),
        pytest.param(None, Department(code="75"), id="departement_seul"),
    ],
)
def test_localisation_abroad_rejects_region_and_department(region, department):
    with pytest.raises(ValueError, match="DEU"):
        Localisation(
            area=GeographicalArea.EUROPE,
            country=Country("DEU"),
            region=region,
            department=department,
        )
