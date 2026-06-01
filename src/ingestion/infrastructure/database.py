import re
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine

_ALEMBIC_INI = Path(__file__).parent.parent / "alembic.ini"


def _make_sync_url(url: str) -> str:
    return re.sub(
        r"^(?:postgresql|postgres|psql)(?:\+\w+)?://", "postgresql+psycopg2://", url
    )


def make_engine(database_url: str) -> Engine:
    return create_engine(_make_sync_url(database_url))


def run_migrations(database_url: str) -> None:
    alembic_cfg = Config(str(_ALEMBIC_INI))
    alembic_cfg.set_main_option("sqlalchemy.url", _make_sync_url(database_url))
    command.upgrade(alembic_cfg, "head")
