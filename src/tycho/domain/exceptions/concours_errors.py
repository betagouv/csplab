"""Domain errors for entity Concours."""

from domain.exceptions.domain_errors import DomainError


class ConcoursError(DomainError):
    """Base exception for Concours domain errors."""

    pass


class ConcoursDoesNotExist(ConcoursError):
    """Raised when a Concours with the given ID does not exist."""

    def __init__(self, concours_id: int):
        """Initialize with the concours ID."""
        super().__init__(f"Concours with ID {concours_id} does not exist")
        self.concours_id = concours_id


class InvalidNorError(ConcoursError):
    """Raised when an invalid nor code is provided."""

    def __init__(self, nor_str: str):
        """Initialize with the invalid nor string."""
        super().__init__(f"Invalid nor code: {nor_str}")
        self.nor_str = nor_str
