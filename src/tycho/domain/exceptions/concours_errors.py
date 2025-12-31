"""Domain errors for entity Concours."""

from domain.exceptions.domain_errors import DomainError


class ConcoursError(DomainError):
    """Base exception for Concours domain errors."""

    pass


class InvalidNorError(ConcoursError):
    """Raised when an invalid nor code is provided."""

    def __init__(self, nor_str: str):
        """Initialize with the invalid nor string."""
        super().__init__(f"Invalid nor code: {nor_str}")
        self.nor_str = nor_str
