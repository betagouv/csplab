import pytest

from referentiel.value_objects.department import Department


@pytest.mark.parametrize(
    ("cog_commune", "expected_code"),
    [
        pytest.param("01053", "01", id="metropole"),
        pytest.param("97120", "971", id="dom"),
        pytest.param("5", None, id="too_short"),
        pytest.param("97", None, id="dom_prefix_without_enough_digits"),
        pytest.param("00042", None, id="invalid_department"),
    ],
)
def test_from_commune_code(cog_commune, expected_code):
    department = Department.from_commune_code(cog_commune)

    if expected_code is None:
        assert department is None
    else:
        assert department is not None
        assert department.code == expected_code
