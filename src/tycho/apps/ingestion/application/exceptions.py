"""Application layer exceptions."""

from apps.shared.exceptions import ApplicationError


class LoadDocumentsError(ApplicationError):
    """Exception for LoadDocuments use case errors."""
