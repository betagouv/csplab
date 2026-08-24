from typing import Protocol

from referentiel.entities.organisme import Organisme


class IPublishOrganismesGateway(Protocol):
    async def publish(self, organismes: list[Organisme]) -> None: ...
