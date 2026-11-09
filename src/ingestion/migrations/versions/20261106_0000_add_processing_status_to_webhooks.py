"""add processing status to webhooks

Revision ID: 8f3b6c2d4e71
Revises: 5c2e7d1a9b40
Create Date: 2026-11-06 00:00:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

revision: str = "8f3b6c2d4e71"
down_revision: Union[str, None] = "5c2e7d1a9b40"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "webhooks",
        sa.Column("processing_status", sqlmodel.AutoString(), nullable=True),
    )
    op.add_column(
        "webhooks",
        sa.Column("attempts", sa.Integer(), server_default="0", nullable=False),
    )
    op.add_column(
        "webhooks", sa.Column("last_error", sqlmodel.AutoString(), nullable=True)
    )
    op.add_column(
        "webhooks",
        sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        op.f("ix_webhooks_processing_status"), "webhooks", ["processing_status"]
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_webhooks_processing_status"), table_name="webhooks")
    op.drop_column("webhooks", "processed_at")
    op.drop_column("webhooks", "last_error")
    op.drop_column("webhooks", "attempts")
    op.drop_column("webhooks", "processing_status")
