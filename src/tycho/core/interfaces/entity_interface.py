"""Entity interface definitions."""

from typing import Protocol


class IEntity(Protocol):
    """Interface for domain entities."""

    id: int
    """Unique identifier for the entity."""
