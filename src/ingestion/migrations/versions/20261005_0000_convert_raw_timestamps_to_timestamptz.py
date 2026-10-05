"""convert raw_offers and raw_organismes timestamps to timestamptz

Revision ID: ab7582a42150
Revises: 3f6a8b1c9d02
Create Date: 2026-10-05 00:00:00.000000+00:00
"""

from typing import Sequence, Union

from alembic import op

revision: str = "ab7582a42150"
down_revision: Union[str, None] = "3f6a8b1c9d02"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

COLUMNS: dict[str, list[str]] = {
    "raw_offers": [
        "created_at",
        "updated_at",
        "loaded_at",
        "cleaned_at",
        "upsert_at",
        "archived_at",
    ],
    "raw_organismes": [
        "loaded_at",
        "cleaned_at",
        "upsert_at",
        "dila_siret_found_at",
    ],
}


def _alter_columns(target_type: str) -> None:
    # Un seul ALTER TABLE par table : chaque changement de type réécrit la table,
    # et les copies intermédiaires ne sont libérées qu'au commit de la transaction.
    for table, columns in COLUMNS.items():
        clauses = ", ".join(
            f"ALTER COLUMN {column} TYPE {target_type} "
            f"USING {column} AT TIME ZONE 'UTC'"
            for column in columns
        )
        op.execute(f"ALTER TABLE {table} {clauses}")


def upgrade() -> None:
    # Les valeurs existantes ont été écrites en UTC : on les interprète comme telles.
    _alter_columns("TIMESTAMP WITH TIME ZONE")


def downgrade() -> None:
    _alter_columns("TIMESTAMP WITHOUT TIME ZONE")
