from dataclasses import dataclass
from datetime import date
from typing import Any


@dataclass(frozen=True)
class OrganismeImportResource:
    url: str
    millesime: date


@dataclass(frozen=True)
class OrganismeData:
    referentiel: str
    external_id: str
    data: dict[str, Any]
