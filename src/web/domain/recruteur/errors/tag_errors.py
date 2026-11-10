from uuid import UUID

from ddd.domain_errors import DomainError


class TagError(DomainError):
    pass


class TagAlreadyExists(TagError):
    def __init__(self, name: str):
        super().__init__(f"L'étiquette « {name} » existe déjà dans cette catégorie")
        self.name = name


class TagNotFound(TagError):
    def __init__(self, tag_id: UUID):
        super().__init__(f"L'étiquette {tag_id} est introuvable")


class TagCategoryMismatch(TagError):
    def __init__(self, tag_id: UUID):
        super().__init__(f"L'étiquette {tag_id} n'est pas une étiquette de note")


class TagAlreadyOnNote(TagError):
    def __init__(self, tag_id: UUID):
        super().__init__(f"L'étiquette {tag_id} est déjà posée sur cette note")


class TagNotOnNote(TagError):
    def __init__(self, tag_id: UUID):
        super().__init__(f"L'étiquette {tag_id} n'est pas posée sur cette note")
