from typing import Protocol, Union
from uuid import UUID


class IEntity(Protocol):
    id: Union[UUID, int]


class IOfferEntity(IEntity, Protocol):
    external_id: str


class IUserEntity(Protocol):
    entity_id: UUID
