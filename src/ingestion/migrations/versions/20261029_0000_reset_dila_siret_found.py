"""reset the DILA SIRET lookup cache of raw_organismes

Revision ID: 5c2e7d1a9b40
Revises: ab7582a42150
Create Date: 2026-10-29 00:00:00.000000+00:00
"""

from typing import Sequence, Union

from alembic import op

revision: str = "5c2e7d1a9b40"
down_revision: Union[str, None] = "ab7582a42150"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # The cache holds the SIRET of the first search result, with no check of
    # the legal category: it must not be reused.
    op.execute(
        "UPDATE raw_organismes SET dila_siret_found = NULL, "
        "dila_siret_found_at = NULL WHERE referentiel = 'DILA'"
    )


def downgrade() -> None:
    pass
