"""Domain errors for entity Concours."""

from domain.exceptions.domain_errors import DomainError


class ConcoursError(DomainError):
    """Base exception for Concours domain errors."""

    pass


class ConcoursDoesNotExist(ConcoursError):
    """Raised when a Concours with the given ID or NOR does not exist."""

    def __init__(self, identifier: str):
        """Initialize with the concours identifier."""
        super().__init__(f"Concours with identifier {identifier} does not exist")
        self.identifier = identifier


class InvalidNorError(ConcoursError):
    """Raised when an invalid nor code is provided."""

    def __init__(self, nor_str: str):
        """Initialize with the invalid nor string."""
        super().__init__(f"Invalid nor code: {nor_str}")
        self.nor_str = nor_str
