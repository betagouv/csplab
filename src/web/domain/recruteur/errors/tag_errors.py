from ddd.domain_errors import DomainError


class TagError(DomainError):
    pass


class InvalidTagName(TagError):
    pass


class TagAlreadyExists(TagError):
    def __init__(self, name: str):
        super().__init__(f"L'étiquette « {name} » existe déjà dans cette catégorie")
        self.name = name
