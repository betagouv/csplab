from typing import Protocol


class ISiretLookupGateway(Protocol):
    def find_siret(self, nom: str) -> str | None: ...
