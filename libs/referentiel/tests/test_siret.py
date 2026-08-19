import pytest
from pydantic import ValidationError

from referentiel.value_objects.siret import SIRET


def test_valid_siret():
    siret = SIRET(code="26060047300342")

    assert siret.code == "26060047300342"
    assert str(siret) == "26060047300342"


def test_siret_too_short_raises():
    with pytest.raises(ValidationError):
        SIRET(code="123")


def test_siret_non_numeric_raises():
    with pytest.raises(ValidationError):
        SIRET(code="2606004730034A")
