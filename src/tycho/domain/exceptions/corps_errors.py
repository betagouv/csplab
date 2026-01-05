"""Domain errors for entity Corps."""

from domain.exceptions.domain_errors import DomainError


class CorpsError(DomainError):
    """Base exception for Corps domain errors."""

    pass


class InvalidDiplomaLevelError(CorpsError):
    """Raised when an invalid diploma level is provided."""

    def __init__(self, diploma_str: str):
        """Initialize with the invalid diploma string."""
        super().__init__(f"Unknown diploma level: {diploma_str}")
        self.diploma_str = diploma_str


class InvalidCategoryError(CorpsError):
    """Raised when an invalid category is provided."""

    def __init__(self, category_str: str):
        """Initialize with the invalid category string."""
        super().__init__(f"Unknown category: {category_str}")
        self.category_str = category_str


class InvalidMinistryError(CorpsError):
    """Raised when an invalid ministry is provided."""

    def __init__(self, ministry_str: str):
        """Initialize with the invalid ministry string."""
        super().__init__(f"Unknown ministry: {ministry_str}")
        self.ministry_str = ministry_str


class InvalidAccessModalityError(CorpsError):
    """Raised when an invalid access modality is provided."""

    def __init__(self, access_modality_str: str):
        """Initialize with the invalid access modality string."""
        super().__init__(f"Unknown access modality: {access_modality_str}")
        self.access_modality_str = access_modality_str
