"""Category value object."""

from enum import Enum


class Category(Enum):
    """Enumeration of Category."""

    APLUS = "APLUS"
    A = "A"
    B = "B"
    C = "C"
    HORS_CATEGORIE = "HORS_CATEGORIE"

    def __str__(self):
        """Return string representation."""
        return self.value
