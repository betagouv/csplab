from concurrent.futures import ThreadPoolExecutor

import pytest
from django.db import connection

from infrastructure.django_apps.referentiel.models.offer_reference_sequence import (
    OfferReferenceSequenceModel,
)

reserve = OfferReferenceSequenceModel.objects.reserve


def test_sequence_starts_at_one(db):
    assert list(reserve(year=2026, count=2)) == [1, 2]


def test_numbers_follow_each_other_across_calls(db):
    reserve(year=2026, count=2)

    assert list(reserve(year=2026, count=3)) == [3, 4, 5]


def test_sequence_restarts_each_year(db):
    reserve(year=2026, count=3)

    assert list(reserve(year=2027, count=1)) == [1]
    assert list(reserve(year=2026, count=1)) == [4]


def test_zero_count_reserves_no_number(db):
    assert list(reserve(year=2026, count=0)) == []


@pytest.mark.django_db(transaction=True)
def test_concurrent_calls_never_share_a_number():
    def allocate(_):
        try:
            return list(reserve(year=2026, count=20))
        finally:
            connection.close()

    with ThreadPoolExecutor(max_workers=5) as executor:
        batches = list(executor.map(allocate, range(10)))

    numbers = [number for batch in batches for number in batch]
    assert sorted(numbers) == list(range(1, 201))
