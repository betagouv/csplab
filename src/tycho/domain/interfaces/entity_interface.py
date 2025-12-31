"""Entity interface definitions."""

from typing import Protocol, Union
from uuid import UUID


class IEntity(Protocol):
    """Interface for domain entities."""

    id: Union[int, UUID]
    """Unique identifier for the entity."""
