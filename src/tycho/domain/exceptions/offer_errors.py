"""Domain errors for entity Offers."""

from datetime import datetime

from domain.exceptions.domain_errors import DomainError


class InvalidLimitDateError(DomainError):
    """Raised when limit date is invalid."""

    def __init__(self, limit_date: datetime):
        """Initialize with invalid limit date."""
        super().__init__(f"Invalid limit date: {limit_date}")


class OfferDoesNotExist(DomainError):
    """Raised when an offer is not found."""

    def __init__(self, offer_id: int):
        """Initialize with offer ID that was not found."""
        super().__init__(f"Offer with ID {offer_id} does not exist")


class InvalidOfferDataFormatError(DomainError):
    """Raised when raw offer data does not match expected TalentSoft format."""

    def __init__(self, offer_reference: str, validation_details: str):
        """Initialize with offer reference and validation error details."""
        super().__init__(
            f"Raw offer data for '{offer_reference}' is invalid: {validation_details}"
        )
