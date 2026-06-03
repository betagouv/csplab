class DomainError(Exception):
    def __init__(
        self,
        message: str,
        details: dict | None = None,
    ):

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
