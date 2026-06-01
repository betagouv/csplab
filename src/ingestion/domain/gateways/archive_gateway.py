from typing import Protocol


class IArchiveGateway(Protocol):
    async def archive(self, reference: str, source_id: str) -> None: ...
