"""add raw_organismes table

Revision ID: 7a1c3e9f4b2d
Revises: 96540e52312c
Create Date: 2026-08-19 00:00:00.000000+00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "7a1c3e9f4b2d"
down_revision: Union[str, None] = "96540e52312c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "raw_organismes",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("referentiel", sqlmodel.AutoString(length=50), nullable=False),
        sa.Column("millesime", sqlmodel.AutoString(length=25), nullable=False),
        sa.Column("external_id", sqlmodel.AutoString(length=50), nullable=False),
        sa.Column("data", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("error_msg", sqlmodel.AutoString(), nullable=True),
        sa.Column("loaded_at", sa.DateTime(), nullable=True),
        sa.Column("cleaned_at", sa.DateTime(), nullable=True),
        sa.Column("upsert_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "referentiel",
            "external_id",
            name="uq_raw_organisme_referentiel_external_id",
        ),
    )
    op.create_index(
        op.f("ix_raw_organismes_referentiel"),
        "raw_organismes",
        ["referentiel"],
        unique=False,
    )
    op.create_index(
        op.f("ix_raw_organismes_external_id"),
        "raw_organismes",
        ["external_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_raw_organismes_external_id"), table_name="raw_organismes")
    op.drop_index(op.f("ix_raw_organismes_referentiel"), table_name="raw_organismes")
    op.drop_table("raw_organismes")
