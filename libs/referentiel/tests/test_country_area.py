import pycountry
import pytest

from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.country_area import _COUNTRIES_BY_AREA, area_for_country


def test_every_country_has_exactly_one_area():
    codes = [code for codes in _COUNTRIES_BY_AREA.values() for code in codes]

    assert len(codes) == len(set(codes))
    assert set(codes) == {country.alpha_3 for country in pycountry.countries}


@pytest.mark.parametrize(
    ("country_code", "expected_area"),
    [
        # Zones Talentsoft gave to offers abroad.
        ("ARG", GeographicalArea.AMERIQUE),
        ("BEL", GeographicalArea.EUROPE),
        ("BHR", GeographicalArea.MOYEN_ORIENT_AFRIQUE_DU_NORD),
        ("BRA", GeographicalArea.AMERIQUE),
        ("CAN", GeographicalArea.AMERIQUE),
        ("CHE", GeographicalArea.EUROPE),
        ("CHN", GeographicalArea.ASIE),
        ("CIV", GeographicalArea.AFRIQUE),
        ("CRI", GeographicalArea.AMERIQUE),
        ("DEU", GeographicalArea.EUROPE),
        ("DOM", GeographicalArea.AMERIQUE),
        ("DZA", GeographicalArea.MOYEN_ORIENT_AFRIQUE_DU_NORD),
        ("EGY", GeographicalArea.MOYEN_ORIENT_AFRIQUE_DU_NORD),
        ("ETH", GeographicalArea.AFRIQUE),
        ("GAB", GeographicalArea.AFRIQUE),
        ("GEO", GeographicalArea.EUROPE),
        ("GIN", GeographicalArea.AFRIQUE),
        ("GRC", GeographicalArea.EUROPE),
        ("GUY", GeographicalArea.AMERIQUE),
        ("IND", GeographicalArea.ASIE),
        ("ITA", GeographicalArea.EUROPE),
        ("KAZ", GeographicalArea.ASIE),
        ("KOR", GeographicalArea.ASIE),
        ("LBN", GeographicalArea.MOYEN_ORIENT_AFRIQUE_DU_NORD),
        ("MAR", GeographicalArea.MOYEN_ORIENT_AFRIQUE_DU_NORD),
        ("MEX", GeographicalArea.AMERIQUE),
        ("MRT", GeographicalArea.AFRIQUE),
        ("NCL", GeographicalArea.OCEANIE),
        ("PHL", GeographicalArea.ASIE),
        ("POL", GeographicalArea.EUROPE),
        ("PSE", GeographicalArea.MOYEN_ORIENT_AFRIQUE_DU_NORD),
        ("PYF", GeographicalArea.OCEANIE),
        ("TCD", GeographicalArea.AFRIQUE),
        ("THA", GeographicalArea.ASIE),
        ("USA", GeographicalArea.AMERIQUE),
        ("VUT", GeographicalArea.OCEANIE),
        # Others.
        ("FRA", GeographicalArea.EUROPE),
        ("TUR", GeographicalArea.EUROPE),
        ("REU", GeographicalArea.AFRIQUE),
        ("ATA", GeographicalArea.ANTARTIQUE),
    ],
)
def test_area_for_country(country_code, expected_area):
    assert area_for_country(Country(country_code)) == expected_area
