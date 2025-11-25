"""Domain layer exceptions."""

from rest_framework import status


class DomainError(Exception):
    """Base exception for domain layer errors (business rules violations)."""

    def __init__(
        self,
        message: str,
        details: dict | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        """Initialize domain error.

        Args:
            message: Error message
            details: Additional error details
            status_code: HTTP status code
        """
        self.message = message
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)

    @property
    def error_type(self) -> str:
        """Generate hierarchical error type from class inheritance."""
        classes = []
        for cls in self.__class__.__mro__:
            if cls is Exception:
                break
            classes.append(cls.__name__)
        return "::".join(reversed(classes))


# Document entity exceptions
class DocumentError(DomainError):
    """Base exception for Document entity errors."""

    pass


class DocumentValidationError(DocumentError):
    """Exception for document validation failures."""

    pass


class InvalidDocumentTypeError(DocumentError):
    """Exception for invalid document type in business rules."""

    def __init__(self, document_type: str):
        """Initialize invalid document type error.

        Args:
            document_type: The invalid document type
        """
        message = f"Invalid document type: {document_type}"
        super().__init__(message)


class MixedDocumentTypesError(DocumentError):
    """Exception for mixed document types in a batch operation."""

    def __init__(self, document_types: set):
        """Initialize mixed document types error.

        Args:
            document_types: The set of mixed document types
        """
        message = (
            f"Mixed document types not supported in batch operation: {document_types}"
        )
        super().__init__(message)


class UnsupportedDocumentTypeError(DocumentError):
    """Exception for unsupported document type in cleaner."""

    def __init__(self, document_type: str):
        """Initialize unsupported document type error.

        Args:
            document_type: The unsupported document type
        """
        message = f"No cleaner available for document type: {document_type}"
        super().__init__(message)
