from dataclasses import dataclass
from uuid import UUID

from ddd.entity import Entity

from domain.ingestion.value_objects.source_type import SourceType


@dataclass(kw_only=True)
class Source(Entity):
    source_id: UUID
    slug: str
    type: SourceType
    client_id_front: str
    client_id_back: str
    base_url_front: str
    base_url_back: str
