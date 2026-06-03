from dataclasses import dataclass, field
from uuid import UUID, uuid4

from ddd.entity import Entity

from domain.ingestion.value_objects.source_type import SourceType


@dataclass(kw_only=True)
class Source(Entity):
    source_id: UUID
    type: SourceType
    client_id_front: str
    client_id_back: str
    base_url_front: str
    base_url_back: str
    id: UUID = field(default_factory=uuid4)
