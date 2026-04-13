from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from domain.interfaces.entity_interface import IEntity


@dataclass
class DomaineFonctionnel(IEntity):
    libelle: str
    description: Optional[str]
    id: UUID = field(default_factory=uuid4)
