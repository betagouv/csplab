from dataclasses import dataclass, field
from uuid import UUID, uuid4

from domain.ddd.entity_interface import IEntity
from domain.value_objects.source_type import SourceType


@dataclass
class Source(IEntity):
    source_id: UUID
    type: SourceType
    client_id_front: str
    client_id_back: str
    base_url_front: str
    base_url_back: str
    id: UUID = field(default_factory=uuid4)
