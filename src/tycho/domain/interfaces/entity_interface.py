from typing import Protocol, Union
from uuid import UUID


class IEntity(Protocol):
    id: Union[int, UUID]
