"""merge webhooks and archived_at

Revision ID: 37a97d8bcec5
Revises: a1b2c3d4e5f6, 8d711cbbc883
Create Date: 2026-06-10 07:51:48.513820+00:00

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "37a97d8bcec5"
down_revision: Union[str, Sequence[str], None] = ("a1b2c3d4e5f6", "8d711cbbc883")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
