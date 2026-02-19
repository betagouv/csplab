"""Tests for LimitDate value object."""

from datetime import datetime, timedelta, timezone

import pytest

from domain.value_objects.limit_date import LimitDate


def test_limit_date_creation_with_valid_datetime():
    """Test LimitDate creation with valid datetime."""
    date = datetime.now(timezone.utc)
    limit_date = LimitDate(date)

    assert limit_date.value == date


@pytest.mark.parametrize(
    "days_offset, expected_expired",
    [
        (-1, True),  # past date
        (1, False),  # future date
    ],
)
def test_is_expired(days_offset, expected_expired):
    """Test is_expired returns correct value for past and future dates."""
    date = datetime.now() + timedelta(days=days_offset)
    limit_date = LimitDate(date)

    assert limit_date.is_expired() is expected_expired


def test_limit_date_is_frozen():
    """Test LimitDate is immutable (frozen dataclass)."""
    date = datetime.now()
    limit_date = LimitDate(date)

    with pytest.raises(AttributeError):
        limit_date.value = datetime.now(timezone.utc)
