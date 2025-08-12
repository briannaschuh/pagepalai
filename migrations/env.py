import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

sys.path.append(os.path.abspath("."))

config = context.config # reads alembic.ini

if config.config_file_name is not None:
    fileConfig(config.config_file_name) # logging

from backend.db.base import Base
from backend.db.models import (
    book,       # noqa: F401
    chunk,      # noqa: F401
    ai_output,  # noqa: F401
    language_level,  # noqa: F401
    language_mapping # noqa: F401
)

target_metadata = Base.metadata

db_url = os.getenv("DATABASE_URL")

# Fallback to the  app's config logic (loads .env and chooses local vs prod)
if not db_url:
    try:
        from backend.config import DATABASE_URL as APP_DB_URL
        db_url = APP_DB_URL
    except Exception:
        db_url = None

if not db_url:
    raise RuntimeError("No database URL set. Set DATABASE_URL or configure backend.config.")

config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (no DBAPI engine)."""
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode (real connection)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
