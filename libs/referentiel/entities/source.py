from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from ddd.entity_interface import IEntity

from referentiel.exceptions.source_errors import MissingTalentsoftFieldsError
from referentiel.value_objects.source_type import SourceType


@dataclass
class Source(IEntity):
    source_id: UUID
    slug: str
    type: SourceType
    client_id_front: Optional[str] = None
    client_id_back: Optional[str] = None
    base_url_front: Optional[str] = None
    base_url_back: Optional[str] = None
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        if self.type == SourceType.TALENTSOFT:
            if not all(
                [
                    self.client_id_front,
                    self.client_id_back,
                    self.base_url_front,
                    self.base_url_back,
                ]
            ):
                raise MissingTalentsoftFieldsError()
