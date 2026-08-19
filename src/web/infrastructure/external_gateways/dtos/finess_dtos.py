from dataclasses import dataclass


@dataclass(frozen=True)
class EtablissementDTO:
    nom: str
    external_id: str
    siret: str
    latitude: float | None
    longitude: float | None
    departement: str | None
    millesime: str
