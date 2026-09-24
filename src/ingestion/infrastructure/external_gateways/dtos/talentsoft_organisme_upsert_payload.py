from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from infrastructure.external_gateways.dtos.talentsoft_dtos import (
    TalentsoftOrganisationPayload,
)


class TalentsoftOrganismeUpsertPayload(BaseModel):
    organisme_id: Optional[UUID] = None
    entity_code: str
    code: str
    parent_code: Optional[str] = None
    has_children: bool = False
    name: str
    description: Optional[str] = None
    url: Optional[str] = None
    phone_number: Optional[str] = None
    post_code: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    parent_name: Optional[str] = None
    logo_url: Optional[str] = None
    max_delay_for_consent: Optional[int] = None
    retention_period: Optional[int] = None
    general_conditions: Optional[str] = None
    personal_data_consent: Optional[str] = None

    @classmethod
    def from_organisation_payload(
        cls, organisation: TalentsoftOrganisationPayload
    ) -> TalentsoftOrganismeUpsertPayload:
        return cls(
            entity_code=organisation.entityCode,
            code=str(organisation.code),
            parent_code=(
                str(organisation.parentCode)
                if organisation.parentCode is not None
                else None
            ),
            has_children=organisation.hasChildren,
            name=organisation.name,
            description=organisation.description,
            url=organisation.url,
            phone_number=organisation.phoneNumber,
            post_code=organisation.postCode,
            latitude=(
                organisation.geolocation.latitude if organisation.geolocation else None
            ),
            longitude=(
                organisation.geolocation.longitude if organisation.geolocation else None
            ),
            parent_name=organisation.parentName,
            logo_url=organisation.logoUrl,
            max_delay_for_consent=organisation.maxDelayForConsent,
            retention_period=organisation.retentionPeriod,
            general_conditions=organisation.generalConditions,
            personal_data_consent=organisation.personalDataConsent,
        )
