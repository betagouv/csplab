class InfrastructureError(Exception):
    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


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
