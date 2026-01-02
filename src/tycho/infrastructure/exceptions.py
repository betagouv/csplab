"""Infrastructure layer exceptions."""


class InfrastructureError(Exception):
    """Base exception for infrastructure layer errors."""

    def __init__(self, message: str, details: dict | None = None):
        """Initialize infrastructure error.

        Args:
            message: Error message
            details: Additional error details
        """
        self.message = message
        self.details = details or {}
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


# External API exceptions
class ExternalApiError(InfrastructureError):
    """Exception for external API errors."""

    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        api_name: str | None = None,
        details: dict | None = None,
    ):
        """Initialize external API error.

        Args:
            message: Error message
            status_code: HTTP status code from API
            api_name: Name of the external API
            details: Additional error details
        """
        self.status_code = status_code
        self.api_name = api_name
        super().__init__(message, details)


# Database exceptions
class DatabaseError(InfrastructureError):
    """Exception for database/persistence errors."""

    def __init__(
        self,
        message: str = "Erreur de base de données",
        details: dict | None = None,
    ):
        """Initialize database error.

        Args:
            message: Error message
            details: Additional error details
        """
        super().__init__(message, details)
