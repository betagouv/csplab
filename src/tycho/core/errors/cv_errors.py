"""CV domain specific errors."""

from core.errors.domain_errors import DomainError


class CVError(DomainError):
    """Base error for CV domain operations."""

    pass


class InvalidPDFError(CVError):
    """Error raised when PDF file is invalid or corrupted."""

    def __init__(self, filename: str, reason: str = "Invalid PDF format"):
        """Initialize InvalidPDFError.

        Args:
            filename: Name of the invalid PDF file
            reason: Specific reason why the PDF is invalid
        """
        self.filename = filename
        self.reason = reason
        super().__init__(f"Invalid PDF file '{filename}': {reason}")


class TextExtractionError(CVError):
    """Error raised when text extraction from PDF fails."""

    def __init__(self, filename: str, reason: str = "Failed to extract text"):
        """Initialize TextExtractionError.

        Args:
            filename: Name of the PDF file where extraction failed
            reason: Specific reason why text extraction failed
        """
        self.filename = filename
        self.reason = reason
        super().__init__(f"Text extraction failed for '{filename}': {reason}")


class QueryBuildingError(CVError):
    """Error raised when query building from CV text fails."""

    def __init__(self, reason: str = "Failed to build search query"):
        """Initialize QueryBuildingError.

        Args:
            reason: Specific reason why query building failed
        """
        self.reason = reason
        super().__init__(f"Query building failed: {reason}")


class CVMetadataSaveError(CVError):
    """Error raised when saving CV metadata fails."""

    def __init__(self, reason: str = "Failed to save CV metadata"):
        """Initialize CVMetadataSaveError.

        Args:
            reason: Specific reason why CV metadata save failed
        """
        self.reason = reason
        super().__init__(f"CV metadata save failed: {reason}")


class CVNotFoundError(CVError):
    """Error raised when CV metadata is not found."""

    def __init__(self, cv_id: str):
        """Initialize CVNotFoundError.

        Args:
            cv_id: ID of the CV metadata that was not found
        """
        self.cv_id = cv_id
        super().__init__(f"CV metadata not found for ID: {cv_id}")
