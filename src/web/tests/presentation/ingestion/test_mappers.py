from datetime import datetime, timezone

import pytest

from presentation.ingestion.mappers import OfferSummaryOutputMapper


@pytest.mark.parametrize(
    "value,expected",
    [
        (None, None),
        (datetime(2024, 1, 15, tzinfo=timezone.utc), "2024-01-15T00:00:00"),
        (
            datetime(2026, 7, 30, 10, 8, 39, 230000, tzinfo=timezone.utc),
            "2026-07-30T10:08:39.23",
        ),
    ],
    ids=[
        "none-value-returns-none",
        "no-microsecond-has-no-fractional-part",
        "microsecond-truncated-to-centiseconds-and-drops-timezone",
    ],
)
def test_isoformat(value, expected):
    assert OfferSummaryOutputMapper._isoformat(value) == expected
