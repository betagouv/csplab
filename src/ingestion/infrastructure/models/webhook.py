from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Index, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


class WebhookModel(SQLModel, table=True):  # type: ignore[call-arg]
    __tablename__ = "webhooks"
    __table_args__ = (
        Index("ix_webhooks_source_id_reference", "source_id", "reference"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime, default=func.now(), nullable=False)
    )
    updated_at: datetime = Field(
        sa_column=Column(
            DateTime, default=func.now(), onupdate=func.now(), nullable=False
        )
    )
    source_id: str
    webhook_type: str = Field(index=True)
    event_type: str = Field(index=True)
    reference: str
    status_id: Optional[str] = None
    action_type: Optional[str] = Field(default=None, index=True)
    payload: dict[str, Any] = Field(sa_column=Column(JSONB, nullable=False))
