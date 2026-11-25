from collections.abc import Mapping
from typing import Protocol
from uuid import UUID

from referentiel.entities.organisme import Organisme


class IPublishOrganismesGateway(Protocol):
    async def publish(
        self, organismes: list[Organisme], external_ids: Mapping[UUID, str | None]
    ) -> None: ...
