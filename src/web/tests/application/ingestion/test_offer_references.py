import pytest

from application.ingestion.services.offer_references import (
    format_reference,
    is_generated_reference,
    unknown_generated_references,
)
from infrastructure.factories.ingestion.source_django_factory import (
    SourceDjangoFactory,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)


@pytest.mark.parametrize(
    "number,expected",
    [
        (1, "CSP-2026-000001"),
        (123456, "CSP-2026-123456"),
        (1234567, "CSP-2026-1234567"),
    ],
)
def test_reference_is_formatted_with_year_and_padded_number(number, expected):
    assert format_reference(2026, number) == expected


@pytest.mark.parametrize(
    "reference,expected",
    [
        ("CSP-2026-000001", True),
        ("CSP-2026-1234567", True),
        ("CSP-2026-00001", False),
        ("REF-2026-000001", False),
        ("CSP-2026-000001-bis", False),
        ("auto", False),
    ],
)
def test_generated_reference_detection(reference, expected):
    assert is_generated_reference(reference) is expected


def test_unknown_generated_references(db):
    source = SourceDjangoFactory()
    OfferDjangoFactory(source=source, reference="CSP-2026-000001")
    OfferDjangoFactory(reference="CSP-2026-000002")

    assert unknown_generated_references(
        source.source_id,
        ["CSP-2026-000001", "CSP-2026-000002", "CSP-2026-000003", "REF-001"],
    ) == {"CSP-2026-000002", "CSP-2026-000003"}


def test_no_query_without_generated_reference(db, django_assert_num_queries):
    with django_assert_num_queries(0):
        assert unknown_generated_references(None, ["REF-001", "auto"]) == set()
