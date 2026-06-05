from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def _now() -> datetime:
    return datetime.now(tz=timezone.utc)


class TalentsoftWebhookModel(SQLModel, table=True):  # type: ignore[call-arg]
    __tablename__ = "talentsoft_webhooks"
    __table_args__ = (
        Index("ix_talentsoft_webhooks_source_id_reference", "source_id", "reference"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=_now)
    updated_at: datetime = Field(default_factory=_now)
    source_id: str
    event_type: str = Field(index=True)
    reference: str
    status_id: Optional[str] = None
    payload: dict[str, Any] = Field(sa_column=Column(JSONB, nullable=False))
