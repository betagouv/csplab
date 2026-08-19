from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


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
