"""convert raw_offers and raw_organismes timestamps to timestamptz

Revision ID: ab7582a42150
Revises: 3f6a8b1c9d02
Create Date: 2026-10-05 00:00:00.000000+00:00
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "ab7582a42150"
down_revision: Union[str, None] = "3f6a8b1c9d02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

COLUMNS: dict[str, list[tuple[str, bool]]] = {
    "raw_offers": [
        ("created_at", False),
        ("updated_at", False),
        ("loaded_at", True),
        ("cleaned_at", True),
        ("upsert_at", True),
        ("archived_at", True),
    ],
    "raw_organismes": [
        ("loaded_at", True),
        ("cleaned_at", True),
        ("upsert_at", True),
        ("dila_siret_found_at", True),
    ],
}


def upgrade() -> None:
    # Les valeurs existantes ont été écrites en UTC : on les interprète comme telles.
    for table, columns in COLUMNS.items():
        for column, nullable in columns:
            op.alter_column(
                table,
                column,
                existing_type=sa.DateTime(),
                type_=sa.DateTime(timezone=True),
                existing_nullable=nullable,
                postgresql_using=f"{column} AT TIME ZONE 'UTC'",
            )


def downgrade() -> None:
    for table, columns in COLUMNS.items():
        for column, nullable in columns:
            op.alter_column(
                table,
                column,
                existing_type=sa.DateTime(timezone=True),
                type_=sa.DateTime(),
                existing_nullable=nullable,
                postgresql_using=f"{column} AT TIME ZONE 'UTC'",
            )
