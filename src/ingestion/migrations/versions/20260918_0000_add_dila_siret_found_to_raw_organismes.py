"""add dila_siret_found columns to raw_organismes

Revision ID: 3f6a8b1c9d02
Revises: 7a1c3e9f4b2d
Create Date: 2026-09-18 00:00:00.000000+00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

revision: str = "3f6a8b1c9d02"
down_revision: Union[str, None] = "7a1c3e9f4b2d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "raw_organismes",
        sa.Column("dila_siret_found", sqlmodel.AutoString(length=14), nullable=True),
    )
    op.add_column(
        "raw_organismes",
        sa.Column("dila_siret_found_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("raw_organismes", "dila_siret_found_at")
    op.drop_column("raw_organismes", "dila_siret_found")
