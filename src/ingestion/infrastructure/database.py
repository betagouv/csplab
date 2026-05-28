import re

from sqlalchemy import Engine, create_engine
from sqlmodel import SQLModel

import infrastructure.models.raw_offer  # noqa: F401 — registers RawOffer with SQLModel metadata


def _make_sync_url(url: str) -> str:
    return re.sub(
        r"^(?:postgresql|postgres|psql)(?:\+\w+)?://", "postgresql+psycopg2://", url
    )


def make_engine(database_url: str) -> Engine:
    return create_engine(_make_sync_url(database_url))


def create_tables(engine: Engine) -> None:
    SQLModel.metadata.create_all(engine)
