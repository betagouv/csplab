"""Domain errors for entity Offers."""

from datetime import datetime

from .domain_errors import DomainError


class InvalidLimitDateError(DomainError):
    """Raised when limit date is invalid."""

    def __init__(self, limit_date: datetime):
        """Initialize with invalid limit date."""
        super().__init__(f"Invalid limit date: {limit_date}")


class MissingCategoryError(DomainError):
    """Raised when category is required but missing."""

    def __init__(self, external_id: str):
        """Initialize with external_id."""
        super().__init__(f"Category is required for offer {external_id}")


class MissingVerseError(DomainError):
    """Raised when verse is required but missing."""

    def __init__(self, external_id: str):
        """Initialize with external_id."""
        super().__init__(f"Verse is required for offer {external_id}")
