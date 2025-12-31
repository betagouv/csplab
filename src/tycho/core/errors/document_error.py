"""Domain errors for entity Document."""

from core.errors.domain_errors import DomainError


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
        message = f"Document type: {document_type} is not supported yet"
        super().__init__(message)
