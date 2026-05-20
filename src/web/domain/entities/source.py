from dataclasses import dataclass
from uuid import UUID

from domain.interfaces.entity_interface import IEntity
from domain.value_objects.source_type import SourceType


@dataclass
class Source(IEntity):
    id: UUID
    type: SourceType
    client_id_front: str
    client_id_back: str
    base_url: str
