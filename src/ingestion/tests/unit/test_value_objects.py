from datetime import datetime, timedelta, timezone

import pytest
from referentiel.exceptions.offer_errors import InvalidLimitDateError
from referentiel.value_objects.area import GeographicalArea
from referentiel.value_objects.country import Country
from referentiel.value_objects.department import Department
from referentiel.value_objects.limit_date import LimitDate
from referentiel.value_objects.localisation import Localisation
from referentiel.value_objects.region import Region

from domain.value_objects.contact import Contact, ContactRole


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
        assert GeographicalArea.MOYEN_ORIENT_AFRIQUE_DU_NORD.value == "MO"


class TestLocalisation:
    def test_str_returns_formatted_string(self):
        localisation = Localisation(
            area=GeographicalArea.EUROPE,
            country=Country("FRA"),
            region=Region(code="11"),
            department=Department(code="75"),
        )
        assert str(localisation) == "France - 11 - 75"


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


class TestContact:
    def test_from_text_strips_text_and_extracts_emails(self):
        contact = Contact.from_text(
            ContactRole.PRINCIPAL,
            "  Camille Martin : camille.martin@exemple.gouv.fr ; 01 23 45 67 89 ",
        )

        assert contact == Contact(
            role=ContactRole.PRINCIPAL,
            text="Camille Martin : camille.martin@exemple.gouv.fr ; 01 23 45 67 89",
            emails=["camille.martin@exemple.gouv.fr"],
        )

    def test_from_text_extracts_several_emails_without_duplicates(self):
        contact = Contact.from_text(
            ContactRole.AUTRE,
            "rh@exemple.fr;camille.martin@exemple.fr ; rh@exemple.fr",
        )

        assert contact is not None
        assert contact.emails == ["rh@exemple.fr", "camille.martin@exemple.fr"]

    def test_from_text_returns_no_email_for_name_only(self):
        contact = Contact.from_text(ContactRole.PRINCIPAL, "Camille Martin")

        assert contact is not None
        assert contact.emails == []

    @pytest.mark.parametrize(
        "text, expected",
        [
            ("chg.tj-paris@justice.fr-Camille MARTIN", ["chg.tj-paris@justice.fr"]),
            ("(camille.martin@exemple.gouv.fr)", ["camille.martin@exemple.gouv.fr"]),
            ("mail : rh@exemple.gouv.fr.", ["rh@exemple.gouv.fr"]),
            ("hélène.martin@exemple.fr", []),
            ("camille.martin@@exemple.fr", []),
            ("camille.martin.@exemple.fr", []),
            ("camille.martin@exemple", []),
        ],
    )
    def test_from_text_only_extracts_valid_emails(self, text, expected):
        contact = Contact.from_text(ContactRole.PRINCIPAL, text)

        assert contact is not None
        assert contact.emails == expected

    @pytest.mark.parametrize("text", [None, "", "   ", ".", " - ; "])
    def test_from_text_returns_none_without_letter_or_digit(self, text):
        assert Contact.from_text(ContactRole.PRINCIPAL, text) is None
