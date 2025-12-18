"""Domain errors for entity Offers."""

from datetime import datetime

from .domain_errors import DomainError


class InvalidLimitDateError(DomainError):
    """Raised when limit date is invalid."""

    def __init__(self, limit_date: datetime):
        """Initialize with invalid limit date."""
        super().__init__(f"Invalid limit date: {limit_date}")
