from uuid import UUID

from domain.exceptions.domain_errors import DomainError


class CorpsError(DomainError):
    pass


class CorpsDoesNotExist(CorpsError):
    def __init__(self, id: UUID | str):
        super().__init__(f"Corps with ID {id} does not exist")
        self.id = id


class InvalidDiplomaLevelError(CorpsError):
    def __init__(self, diploma_str: str):
        super().__init__(f"Unknown diploma level: {diploma_str}")
        self.diploma_str = diploma_str


class InvalidCategoryError(CorpsError):
    def __init__(self, category_str: str):
        super().__init__(f"Unknown category: {category_str}")
        self.category_str = category_str


class InvalidMinistryError(CorpsError):
    def __init__(self, ministry_str: str):
        super().__init__(f"Unknown ministry: {ministry_str}")
        self.ministry_str = ministry_str


class InvalidAccessModalityError(CorpsError):
    def __init__(self, access_modality_str: str):
        super().__init__(f"Unknown access modality: {access_modality_str}")
        self.access_modality_str = access_modality_str
