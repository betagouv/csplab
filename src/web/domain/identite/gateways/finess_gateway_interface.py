from dataclasses import dataclass
from datetime import date
from typing import Iterator, Protocol


@dataclass(frozen=True)
class FinessResource:
    url: str
    millesime: date


@dataclass(frozen=True)
class FinessEtablissement:
    nom: str
    external_id: str
    siret: str
    latitude: float | None
    longitude: float | None
    departement: str | None


class IFinessGateway(Protocol):
    def find_latest_journalier(self) -> FinessResource: ...

    def stream_etablissements(self, url: str) -> Iterator[FinessEtablissement]: ...
