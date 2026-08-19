from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

from domain.entities.raw_organisme import RawOrganisme


class RawOrganismeModel(SQLModel, table=True):  # type: ignore[call-arg]
    __tablename__ = "raw_organismes"
    __table_args__ = (
        UniqueConstraint(
            "referentiel",
            "external_id",
            name="uq_raw_organisme_referentiel_external_id",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    referentiel: str = Field(sa_column=Column(String(50), nullable=False, index=True))
    millesime: str = Field(sa_column=Column(String(25), nullable=False))
    external_id: str = Field(sa_column=Column(String(50), nullable=False, index=True))
    data: Optional[dict[str, Any]] = Field(
        default=None, sa_column=Column(JSONB, nullable=True)
    )
    error_msg: Optional[str] = None
    loaded_at: Optional[datetime] = None
    cleaned_at: Optional[datetime] = None
    upsert_at: Optional[datetime] = None

    def to_entity(self) -> RawOrganisme:
        return RawOrganisme(
            id=self.id,
            referentiel=self.referentiel,
            millesime=self.millesime,
            external_id=self.external_id,
            data=self.data,
            error_msg=self.error_msg,
            loaded_at=self.loaded_at,
            cleaned_at=self.cleaned_at,
            upsert_at=self.upsert_at,
        )

    @staticmethod
    def values_from_entity(organisme: RawOrganisme) -> dict[str, Any]:
        return {
            "id": organisme.id,
            "referentiel": organisme.referentiel,
            "millesime": organisme.millesime,
            "external_id": organisme.external_id,
            "data": organisme.data,
            "error_msg": organisme.error_msg,
            "loaded_at": organisme.loaded_at,
            "cleaned_at": organisme.cleaned_at,
            "upsert_at": organisme.upsert_at,
        }
