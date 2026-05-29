import os
import re
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

# Register all models with SQLModel metadata before Alembic reads it.
import infrastructure.models.raw_offer  # noqa: F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# SQLModel exposes the shared SQLAlchemy metadata that all table=True models
# register themselves into.
target_metadata = SQLModel.metadata


def _get_url() -> str:
    """Return the database URL.

    Priority:
    1. Value set programmatically via ``config.set_main_option("sqlalchemy.url", ...)``
       — used when Alembic is invoked from within the app (run_migrations).
    2. DATABASE_URL environment variable — used when invoking Alembic from the CLI.
    """
    url = config.get_main_option("sqlalchemy.url")
    if url:
        return url
    env_url = os.environ.get("DATABASE_URL")
    if not env_url:
        raise RuntimeError(
            "No database URL configured. "
            "Set DATABASE_URL in your environment or pass it programmatically."
        )
    # Normalise to the synchronous psycopg2 driver (mirrors infrastructure/database.py).
    return re.sub(
        r"^(?:postgresql|postgres|psql)(?:\+\w+)?://", "postgresql+psycopg2://", env_url
    )


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL and not an Engine, though an
    Engine is acceptable here as well.  By skipping the Engine creation we
    don't even need a DBAPI to be available.
    """
    url = _get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine and associate a connection
    with the context.
    """
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = _get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
