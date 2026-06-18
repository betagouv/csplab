import pytest

from domain.identite.errors.organisme_errors import SiretInvalide
from domain.identite.value_objects.siret import SIRET


def test_invalid_siret():
    with pytest.raises(SiretInvalide):
        SIRET("12345678")

    with pytest.raises(SiretInvalide):
        SIRET("1234567890")

    with pytest.raises(SiretInvalide):
        SIRET("12345678A")


def test_valid_siret():
    siret = SIRET("12000201900020")
    assert siret.is_valid() is True
    assert siret.value == "12000201900020"
    assert siret.siren == "120002019"
