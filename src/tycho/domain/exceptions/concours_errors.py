from domain.exceptions.domain_errors import DomainError


class ConcoursError(DomainError):
    pass


class ConcoursDoesNotExist(ConcoursError):
    def __init__(self, identifier: str):
        super().__init__(f"Concours with identifier {identifier} does not exist")
        self.identifier = identifier


class InvalidNorError(ConcoursError):
    """Raised when an invalid nor code is provided."""

    def __init__(self, nor_str: str):
        """Initialize with the invalid nor string."""
        super().__init__(f"Invalid nor code: {nor_str}")
        self.nor_str = nor_str
