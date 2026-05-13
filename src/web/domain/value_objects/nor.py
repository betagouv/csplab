"""NOR value object."""

import re
from dataclasses import dataclass

from domain.exceptions.concours_errors import InvalidNorError


@dataclass(frozen=True)
class NOR:
    """NOR value object with validation and parsing capabilities."""

    value: str

    def __post_init__(self):
        """Validate NOR format."""
        if not self.is_valid():
            raise InvalidNorError(f"Invalid NOR format: {self.value}")

    def is_valid(self) -> bool:
        """Validate NOR format with regex."""
        pattern = r"^[A-Z]{4}\d{7}[A-Z]$"
        return bool(re.match(pattern, self.value))

    def extract_year(self) -> int:
        """Extract year from NOR (positions 4-5)."""
        return int(self.value[4:6]) + 2000  # Assuming 20XX format

    def extract_sequence(self) -> int:
        """Extract sequence number for chronological sorting."""
        return int(self.value[6:11])
