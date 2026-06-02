from datetime import datetime, timedelta, timezone

import pytest

from domain.exceptions.offer_errors import InvalidLimitDateError
from domain.value_objects.area import GeographicalArea
from domain.value_objects.country import Country
from domain.value_objects.department import Department
from domain.value_objects.limit_date import LimitDate
from domain.value_objects.localisation import Localisation
from domain.value_objects.region import Region


class TestLimitDate:
    def test_valid_datetime_is_accepted(self):
        dt = datetime(2026, 1, 1, tzinfo=timezone.utc)
        ld = LimitDate(value=dt)
        assert ld.value == dt

    def test_raises_invalid_limit_date_error_when_not_datetime(self):
        with pytest.raises(InvalidLimitDateError):
            LimitDate(value="not-a-datetime")  # type: ignore[arg-type]

    def test_is_expired_returns_true_when_in_past(self):
        past = datetime.now(timezone.utc) - timedelta(days=1)
        assert LimitDate(value=past).is_expired() is True

    def test_is_expired_returns_false_when_in_future(self):
        future = datetime.now(timezone.utc) + timedelta(days=1)
        assert LimitDate(value=future).is_expired() is False


class TestRegion:
    def test_str_returns_code(self):
        assert str(Region(code="11")) == "11"

    def test_name_returns_human_readable(self):
        assert Region(code="11").name == "Île-de-France"

    def test_name_returns_code_for_unknown(self):
        # DOM and TOM are valid codes but have no name entry
        assert Region(code="DOM").name == "DOM"

    def test_invalid_code_raises(self):
        with pytest.raises(ValueError, match="Invalid French region INSEE code"):
            Region(code="INVALID")


class TestGeographicalArea:
    def test_str_returns_value(self):
        assert str(GeographicalArea.EUROPE) == "EU"

    def test_all_values_accessible(self):
        assert GeographicalArea.AFRIQUE.value == "AF"
        assert GeographicalArea.ASIE.value == "AS"
        assert GeographicalArea.AMERIQUE.value == "AM"
        assert GeographicalArea.OCEANIE.value == "OC"
        assert GeographicalArea.ANTARTIQUE.value == "AN"


class TestLocalisation:
    def test_str_returns_formatted_string(self):
        localisation = Localisation(
            area=GeographicalArea.EUROPE,
            country=Country("FRA"),
            region=Region(code="11"),
            department=Department(code="75"),
        )
        assert str(localisation) == "FRA - 11 - 75"


class TestDepartment:
    def test_str_returns_code(self):
        assert str(Department(code="75")) == "75"

    def test_name_returns_human_readable(self):
        assert Department(code="75").name == "Paris"

    def test_name_returns_code_for_unknown_valid(self):
        # SPM is valid but has no entry in NAMES
        assert Department(code="SPM").name == "SPM"

    def test_invalid_code_raises(self):
        with pytest.raises(ValueError, match="Invalid French department code"):
            Department(code="INVALID")
