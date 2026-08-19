from referentiel.value_objects.department import Department


def test_from_commune_code_metropole():
    department = Department.from_commune_code("01053")

    assert department is not None
    assert department.code == "01"


def test_from_commune_code_dom():
    department = Department.from_commune_code("97120")

    assert department is not None
    assert department.code == "971"


def test_from_commune_code_too_short_returns_none():
    assert Department.from_commune_code("5") is None


def test_from_commune_code_dom_prefix_without_enough_digits_returns_none():
    assert Department.from_commune_code("97") is None


def test_from_commune_code_invalid_department_returns_none():
    assert Department.from_commune_code("00042") is None
