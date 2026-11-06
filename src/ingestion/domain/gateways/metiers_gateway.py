from typing import Protocol


class IMetiersGateway(Protocol):
    async def fetch_metiers_multi_domaines(self) -> set[str]: ...
