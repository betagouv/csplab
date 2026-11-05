from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region

from presentation.candidate.filter_config import format_location_value
from presentation.candidate.formatters import (
    format_location_display,
    format_locations_display,
)

PARIS = Localisation(
    area=GeographicalArea.EUROPE,
    country=Country("FRA"),
    region=Region(code="11"),
    department=Department(code="75"),
)
BERLIN = Localisation(
    area=GeographicalArea.EUROPE,
    country=Country("DEU"),
    region=None,
    department=None,
    label="Ambassade de France à Berlin",
)


def test_location_in_france_is_displayed_as_its_department():
    assert format_location_display(PARIS) == "Paris"
    assert format_location_value(PARIS) == "75"


def test_location_abroad_is_displayed_as_its_country_in_french():
    assert format_location_display(BERLIN) == "Allemagne"


def test_location_abroad_has_no_department_filter_value():
    assert format_location_value(BERLIN) == ""


def test_several_locations_display_the_main_one_and_the_number_of_others():
    assert format_locations_display([PARIS, BERLIN, PARIS]) == "Paris + 2"


def test_single_location_displays_only_the_main_one():
    assert format_locations_display([BERLIN]) == "Allemagne"


def test_no_location_displays_nothing():
    assert format_locations_display([]) == ""
