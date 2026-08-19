from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.departement_region import (
    region_et_zone_pour_departement,
)
from referentiel.value_objects.department import Department


def test_region_et_zone_pour_departement_metropole():
    region_et_zone = region_et_zone_pour_departement(Department(code="01"))

    assert region_et_zone is not None
    region, area = region_et_zone
    assert region.code == "84"
    assert area == GeographicalArea.EUROPE


def test_region_et_zone_pour_departement_corse():
    region_et_zone = region_et_zone_pour_departement(Department(code="2A"))

    assert region_et_zone is not None
    region, _ = region_et_zone
    assert region.code == "94"


def test_region_et_zone_pour_departement_dom():
    region_et_zone = region_et_zone_pour_departement(Department(code="971"))

    assert region_et_zone is not None
    region, area = region_et_zone
    assert region.code == "01"
    assert area == GeographicalArea.AMERIQUE


def test_region_et_zone_pour_departement_inconnu():
    # Saint-Pierre-et-Miquelon: code de département valide, non couvert par
    # la table de correspondance région/zone.
    assert region_et_zone_pour_departement(Department(code="975")) is None
