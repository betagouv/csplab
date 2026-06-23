from typing import Protocol

from referentiel.entities.source import Source


class ISourcesGateway(Protocol):
    async def fetch_sources(self) -> list[Source]: ...
