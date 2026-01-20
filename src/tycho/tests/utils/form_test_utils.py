"""Form testing utilities."""


def assert_form_error_code(response, field_name, expected_code):
    """Assert that a specific form error code is present."""
    form = response.context["form"]
    assert form.errors, "Expected form errors but found none"
    field_errors = form.errors.as_data().get(field_name, [])
    assert any(error.code == expected_code for error in field_errors), (
        f"Error code '{expected_code}' not found for field '{field_name}'"
    )
