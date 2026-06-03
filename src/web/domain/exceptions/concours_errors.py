from ddd.domain_errors import DomainError


class ConcoursError(DomainError):
    pass


class ConcoursDoesNotExist(ConcoursError):
    def __init__(self, identifier: str):
        super().__init__(f"Concours with identifier {identifier} does not exist")
        self.identifier = identifier


class InvalidNorError(ConcoursError):
    def __init__(self, nor_str: str):
        super().__init__(f"Invalid nor code: {nor_str}")
        self.nor_str = nor_str
