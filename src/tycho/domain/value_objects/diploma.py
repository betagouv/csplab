"""Diploma value object."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Diploma:
    """Represent diploma for a Corps Entity."""

    MAX_DIPLOMA_LEVEL = 8
    MIN_DIPLOMA_LEVEL = 1

    value: int  # 1-8=CNCP levels

    def __new__(cls, value: int):
        """Validate diploma level."""
        if not isinstance(value, int):
            raise ValueError("Diploma level must be an integer")
        if value < cls.MIN_DIPLOMA_LEVEL or value > cls.MAX_DIPLOMA_LEVEL:
            raise ValueError("Diploma level must be between 1 and 8")

        return super().__new__(cls)

    def __str__(self) -> str:
        """Return the diploma value."""
        return str(self.value)
