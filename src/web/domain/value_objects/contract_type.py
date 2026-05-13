"""Contract type value object."""

from enum import Enum


class ContractType(Enum):
    """Enumeration of contract types."""

    TITULAIRE_CONTRACTUEL = "TITULAIRE_CONTRACTUEL"
    CONTRACTUELS = "CONTRACTUELS"
    TERRITORIAL = "TERRITORIAL"

    def __str__(self):
        """Return string representation."""
        return self.value
