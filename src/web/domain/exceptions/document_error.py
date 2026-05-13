"""Domain errors for entity Document."""

from domain.exceptions.domain_errors import DomainError


class DocumentError(DomainError):
    pass


class DocumentValidationError(DocumentError):
    pass


class InvalidDocumentTypeError(DocumentError):
    def __init__(self, document_type: str):
        message = f"Invalid document type: {document_type}"
        super().__init__(message)


class MixedDocumentTypesError(DocumentError):
    def __init__(self, document_types: set):
        message = (
            f"Mixed document types not supported in batch operation: {document_types}"
        )
        super().__init__(message)


class UnsupportedDocumentTypeError(DocumentError):
    def __init__(self, document_type: str):
        message = f"Document type: {document_type} is not supported yet"
        super().__init__(message)
