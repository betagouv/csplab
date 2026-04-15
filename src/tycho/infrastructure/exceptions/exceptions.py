class InfrastructureError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    @property
    def error_type(self) -> str:
        classes = []
        for cls in self.__class__.__mro__:
            if cls is Exception:
                break
            classes.append(cls.__name__)
        return "::".join(reversed(classes))


# External API exceptions
class ExternalApiError(InfrastructureError):
    def __init__(
        self,
        message: str,
        status_code: int | None = None,
        api_name: str | None = None,
        details: dict | None = None,
    ):
        self.status_code = status_code
        self.api_name = api_name
        super().__init__(message, details)


# Database exceptions
class DatabaseError(InfrastructureError):
    def __init__(
        self,
        message: str = "Erreur de base de données",
        details: dict | None = None,
    ):
        super().__init__(message, details)


# Task exceptions
class TaskError(InfrastructureError):
    def __init__(
        self,
        message: str,
        details: dict | None = None,
    ):
        super().__init__(message, details)
