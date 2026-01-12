"""Tests for LimitDate value object."""

from datetime import datetime, timedelta

import pytest

from domain.value_objects.limit_date import LimitDate


def test_limit_date_creation_with_valid_datetime():
    """Test LimitDate creation with valid datetime."""
    date = datetime.now()
    limit_date = LimitDate(date)

    assert limit_date.value == date


def test_is_expired_with_past_date():
    """Test is_expired returns True for past dates."""
    past_date = datetime.now() - timedelta(days=1)
    limit_date = LimitDate(past_date)

    assert limit_date.is_expired() is True


def test_is_expired_with_future_date():
    """Test is_expired returns False for future dates."""
    future_date = datetime.now() + timedelta(days=1)
    limit_date = LimitDate(future_date)

    assert limit_date.is_expired() is False


def test_limit_date_is_frozen():
    """Test LimitDate is immutable (frozen dataclass)."""
    date = datetime.now()
    limit_date = LimitDate(date)

    with pytest.raises(AttributeError):
        limit_date.value = datetime.now()
