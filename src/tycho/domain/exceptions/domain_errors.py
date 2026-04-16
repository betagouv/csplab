from rest_framework import status


class DomainError(Exception):
    def __init__(
        self,
        message: str,
        details: dict | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):

        self.message = message
        self.details = details or {}
        self.status_code = status_code
        super().__init__(self.message)

    @property
    def error_type(self) -> str:
        classes = []
        for cls in self.__class__.__mro__:
            if cls is Exception:
                break
            classes.append(cls.__name__)
        return "::".join(reversed(classes))


class MetierDoesNotExist(DomainError):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)
