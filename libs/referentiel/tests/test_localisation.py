from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation


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
