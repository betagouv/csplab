"""initial raw_offers table

Revision ID: 3f8a92d1c04e
Revises:
Create Date: 2025-05-29 00:00:00.000000+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3f8a92d1c04e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "raw_offers",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("reference", sqlmodel.AutoString(), nullable=False),
        sa.Column("source_id", sqlmodel.AutoString(), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error_msg", sqlmodel.AutoString(), nullable=True),
        sa.Column("loaded_at", sa.DateTime(), nullable=True),
        sa.Column("cleaned_at", sa.DateTime(), nullable=True),
        sa.Column("upsert_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "reference", "source_id", name="uq_raw_offer_reference_source"
        ),
    )
    op.create_index(
        op.f("ix_raw_offers_reference"), "raw_offers", ["reference"], unique=False
    )
    op.create_index(
        op.f("ix_raw_offers_source_id"), "raw_offers", ["source_id"], unique=False
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_raw_offers_source_id"), table_name="raw_offers")
    op.drop_index(op.f("ix_raw_offers_reference"), table_name="raw_offers")
    op.drop_table("raw_offers")
