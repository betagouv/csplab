from dataclasses import dataclass


@dataclass
class OrganismeDeleteData:
    referentiel: str
    external_id: str


@dataclass
class SupprimerOrganismesInput:
    organismes: list[OrganismeDeleteData]
