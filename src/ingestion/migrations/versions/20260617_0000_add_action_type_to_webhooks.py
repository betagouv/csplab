"""add action_type to webhooks

Revision ID: 96540e52312c
Revises: 37a97d8bcec5
Create Date: 2026-06-17 00:00:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "96540e52312c"
down_revision: Union[str, None] = "37a97d8bcec5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "webhooks",
        sa.Column("action_type", sqlmodel.AutoString(), nullable=True),
    )
    op.create_index(
        op.f("ix_webhooks_action_type"),
        "webhooks",
        ["action_type"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_webhooks_action_type"), table_name="webhooks")
    op.drop_column("webhooks", "action_type")
