"""LimitDate value object."""

from dataclasses import dataclass
from datetime import datetime

from domain.exceptions.offer_errors import InvalidLimitDateError


@dataclass(frozen=True)
class LimitDate:
    """Value object representing a deadline date."""

    value: datetime

    def __post_init__(self):
        """Validate limit date after initialization."""
        if not isinstance(self.value, datetime):
            raise InvalidLimitDateError(self.value)

    def is_expired(self) -> bool:
        """Check if the deadline has passed."""
        return datetime.now() > self.value
