from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


class RawOfferModel(SQLModel, table=True):  # type: ignore[call-arg]
    __tablename__ = "raw_offers"
    __table_args__ = (
        UniqueConstraint(
            "reference", "source_id", name="uq_raw_offer_reference_source"
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    reference: str = Field(index=True)
    source_id: str = Field(index=True)
    data: Optional[dict[str, Any]] = Field(
        default=None, sa_column=Column(JSONB, nullable=True)
    )
    error_msg: Optional[str] = None
    loaded_at: Optional[datetime] = None
    cleaned_at: Optional[datetime] = None
    upsert_at: Optional[datetime] = None
