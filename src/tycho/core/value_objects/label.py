"""Label value object for Corps Entity."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Label:
    """Represent label for a Corps Entity."""

    MAX_LONG_LABEL_LENGTH = 150
    MAX_SHORT_LABEL_LENGTH = 50

    short_value: str
    value: str  # long label by default

    def __new__(cls, short_value: str, value: str):
        """Validate label lengths."""
        if not value:
            raise ValueError("Label is required")
        if not short_value:
            raise ValueError("Short Label is required")
        if len(value) > cls.MAX_LONG_LABEL_LENGTH:
            raise ValueError("Label must be 150 characters or less")
        if len(value) > cls.MAX_SHORT_LABEL_LENGTH:
            raise ValueError("Short label must be 50 characters or less")
        return super().__new__(cls)

    @property
    def short(self) -> str:
        """Return short label."""
        return self.short_value

    def __str__(self) -> str:
        """Return the long label."""
        return self.value
