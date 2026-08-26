import pytest

from referentiel.value_objects.department import Department


@pytest.mark.parametrize(
    ("cog_commune", "expected_code"),
    [
        pytest.param("01053", "01", id="metropole"),
        pytest.param("97120", "971", id="dom"),
    ],
)
def test_from_commune_code(cog_commune, expected_code):
    department = Department.from_commune_code(cog_commune)

    assert department.code == expected_code


@pytest.mark.parametrize(
    "cog_commune",
    [
        pytest.param("5", id="too_short"),
        pytest.param("97", id="dom_prefix_without_enough_digits"),
        pytest.param("00042", id="invalid_department"),
    ],
)
def test_from_commune_code_raises_on_invalid_code(cog_commune):
    with pytest.raises(ValueError):
        Department.from_commune_code(cog_commune)
