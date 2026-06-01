from typing import Protocol

from domain.value_objects.source import Source


class ISourcesGateway(Protocol):
    async def fetch_sources(self) -> list[Source]: ...
