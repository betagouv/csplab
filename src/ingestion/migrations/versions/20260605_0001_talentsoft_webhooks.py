"""webhooks table

Revision ID: a1b2c3d4e5f6
Revises: 3f8a92d1c04e
Create Date: 2026-06-05 00:00:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "3f8a92d1c04e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "webhooks",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("source_id", sqlmodel.AutoString(), nullable=False),
        sa.Column("webhook_type", sqlmodel.AutoString(), nullable=False),
        sa.Column("event_type", sqlmodel.AutoString(), nullable=False),
        sa.Column("reference", sqlmodel.AutoString(), nullable=False),
        sa.Column("status_id", sqlmodel.AutoString(), nullable=True),
        sa.Column("payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_webhooks_source_id_reference",
        "webhooks",
        ["source_id", "reference"],
        unique=False,
    )
    op.create_index(
        op.f("ix_webhooks_webhook_type"),
        "webhooks",
        ["webhook_type"],
        unique=False,
    )
    op.create_index(
        op.f("ix_webhooks_event_type"),
        "webhooks",
        ["event_type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_webhooks_event_type"), table_name="webhooks")
    op.drop_index(op.f("ix_webhooks_webhook_type"), table_name="webhooks")
    op.drop_index("ix_webhooks_source_id_reference", table_name="webhooks")
    op.drop_table("webhooks")
