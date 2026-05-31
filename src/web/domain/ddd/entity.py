from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass()
class Entity:
    entity_id: UUID = field(default_factory=uuid4)
