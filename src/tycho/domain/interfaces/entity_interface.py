from typing import Protocol, Union
from uuid import UUID


class IEntity(Protocol):
    id: Union[int, UUID]


class IOfferEntity(IEntity, Protocol):
    external_id: str
