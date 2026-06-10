"""add archived_at to raw_offers

Revision ID: 8d711cbbc883
Revises: 3f8a92d1c04e
Create Date: 2026-06-06 00:00:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8d711cbbc883"
down_revision: Union[str, None] = "3f8a92d1c04e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "raw_offers",
        sa.Column("archived_at", sa.DateTime(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("raw_offers", "archived_at")
