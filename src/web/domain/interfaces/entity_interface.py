from typing import Protocol
from uuid import UUID


class IEntity(Protocol):
    id: UUID


class IOfferEntity(IEntity, Protocol):
    external_id: str


class IUserEntity(Protocol):
    entity_id: UUID
