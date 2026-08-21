from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel
from referentiel.entities.organisme import Organisme


class LocalisationPayload(BaseModel):
    zone_geographique: str
    pays: str
    region: str
    departement: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class OrganismeUpsertPayload(BaseModel):
    id: str
    nom: str
    versant: str
    siret: str
    parent_id: Optional[str] = None
    external_id: Optional[str] = None
    referentiel: Optional[str] = None
    millesime: Optional[str] = None
    gestion_ats: Optional[bool] = None
    date_creation: Optional[date] = None
    date_derniere_activite: Optional[date] = None
    localisation: Optional[LocalisationPayload] = None

    @classmethod
    def from_organisme(cls, organisme: Organisme) -> OrganismeUpsertPayload:
        localisation = None
        if organisme.localisation:
            localisation = LocalisationPayload(
                zone_geographique=organisme.localisation.area.value,
                pays=str(organisme.localisation.country),
                region=organisme.localisation.region.code,
                departement=organisme.localisation.department.code,
                latitude=organisme.localisation.latitude,
                longitude=organisme.localisation.longitude,
            )

        return cls(
            id=str(organisme.entity_id),
            nom=organisme.nom,
            versant=organisme.versant.value,
            siret=str(organisme.siret),
            parent_id=str(organisme.parent_id) if organisme.parent_id else None,
            external_id=organisme.external_id,
            referentiel=organisme.referentiel,
            millesime=organisme.millesime,
            gestion_ats=organisme.gestion_ats,
            date_creation=organisme.date_creation,
            date_derniere_activite=organisme.date_derniere_activite,
            localisation=localisation,
        )
