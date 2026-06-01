from typing import Protocol

from domain.source import Source


class ISourcesGateway(Protocol):
    async def fetch_sources(self) -> list[Source]: ...
