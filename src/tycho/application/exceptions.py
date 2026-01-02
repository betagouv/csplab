"""Application layer exceptions."""


class ApplicationError(Exception):
    """Base exception for application layer errors."""

    def __init__(
        self,
        message: str,
        details: dict | None = None,
        status_code: int | None = None,
    ):
        """Initialize application error.

        Args:
            message: Error message
            details: Additional error details
            status_code: HTTP status code (defaults to 500 via Django)
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
