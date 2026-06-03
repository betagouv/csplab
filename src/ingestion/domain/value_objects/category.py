from enum import Enum


class Category(Enum):
    APLUS = "APLUS"
    A = "A"
    B = "B"
    C = "C"
    HORS_CATEGORIE = "HORS_CATEGORIE"

    def __str__(self):
        return self.value
