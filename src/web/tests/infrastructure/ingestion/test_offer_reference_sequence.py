from concurrent.futures import ThreadPoolExecutor
from importlib import import_module

import pytest
from django.db import connection

from infrastructure.django_apps.referentiel.models.offer_reference_sequence import (
    OfferReferenceSequenceModel,
    format_reference,
)
from infrastructure.factories.referentiel.offer_django_factory import (
    OfferDjangoFactory,
)

next_references = OfferReferenceSequenceModel.objects.next_references

migration = import_module(
    "infrastructure.django_apps.referentiel.migrations.0051_offer_reference_sequence"
)


def _initialize_sequences():
    with connection.cursor() as cursor:
        cursor.execute(migration.INITIALIZE_SEQUENCES_SQL)


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


def test_references_follow_each_other_across_calls(db):
    assert next_references(year=2026, count=2) == ["CSP-2026-000001", "CSP-2026-000002"]
    assert next_references(year=2026, count=3) == [
        "CSP-2026-000003",
        "CSP-2026-000004",
        "CSP-2026-000005",
    ]


def test_sequence_restarts_each_year(db):
    next_references(year=2026, count=3)

    assert next_references(year=2027, count=1) == ["CSP-2027-000001"]
    assert next_references(year=2026, count=1) == ["CSP-2026-000004"]


def test_references_already_used_by_an_offer_are_skipped(db):
    OfferDjangoFactory(reference="CSP-2026-000002")
    OfferDjangoFactory(reference="CSP-2026-000003")

    assert next_references(year=2026, count=3) == [
        "CSP-2026-000001",
        "CSP-2026-000004",
        "CSP-2026-000005",
    ]


def test_excluded_references_are_skipped(db):
    assert next_references(year=2026, count=2, exclude={"CSP-2026-000001"}) == [
        "CSP-2026-000002",
        "CSP-2026-000003",
    ]


def test_zero_count_returns_no_reference(db):
    assert next_references(year=2026, count=0) == []


@pytest.mark.django_db(transaction=True)
def test_concurrent_calls_never_share_a_reference():
    def allocate(_):
        try:
            return next_references(year=2026, count=20)
        finally:
            connection.close()

    with ThreadPoolExecutor(max_workers=5) as executor:
        batches = list(executor.map(allocate, range(10)))

    references = [reference for batch in batches for reference in batch]
    assert sorted(references) == [format_reference(2026, n) for n in range(1, 201)]


def test_migration_starts_each_year_after_the_highest_existing_reference(db):
    OfferDjangoFactory(reference="CSP-2025-000120")
    OfferDjangoFactory(reference="CSP-2026-000007")
    OfferDjangoFactory(reference="CSP-2026-000042")
    OfferDjangoFactory(reference="CSP-2026-00099")
    OfferDjangoFactory(reference="CSP-2026-1234567")
    OfferDjangoFactory(reference="REF-2026-000500")
    OfferDjangoFactory(reference="2026-999999")

    _initialize_sequences()

    assert next_references(year=2025, count=1) == ["CSP-2025-000121"]
    assert next_references(year=2026, count=1) == ["CSP-2026-000043"]
    assert next_references(year=2027, count=1) == ["CSP-2027-000001"]


def test_migration_never_lowers_an_existing_sequence(db):
    next_references(year=2026, count=50)
    OfferDjangoFactory(reference="CSP-2026-000010")

    _initialize_sequences()

    assert next_references(year=2026, count=1) == ["CSP-2026-000051"]
