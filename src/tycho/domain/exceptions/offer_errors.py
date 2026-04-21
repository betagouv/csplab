from datetime import datetime
from uuid import UUID

from domain.exceptions.domain_errors import DomainError


class InvalidLimitDateError(DomainError):
    def __init__(self, limit_date: datetime):
        super().__init__(f"Invalid limit date: {limit_date}")


class OfferDoesNotExist(DomainError):
    def __init__(self, offer_id: UUID | str):
        super().__init__(f"Offer with ID {offer_id} does not exist")


class InvalidOfferDataFormatError(DomainError):
    def __init__(self, offer_reference: str, validation_details: str):
        super().__init__(
            f"Raw offer data for '{offer_reference}' is invalid: {validation_details}"
        )
