"""Verse value object."""

from enum import Enum


class Verse(Enum):
    """Enumeration of Verse."""

    FPT = "FPT"
    FPE = "FPE"
    FPH = "FPH"

    def __str__(self):
        """Return string representation."""
        return self.value
