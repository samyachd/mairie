from __future__ import annotations

from logging.config import fileConfig
import os
import hashlib

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True), override=True)  # <-- AVANT settings

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from backend.db.db import Base
import backend.db.models  # important: assure que les modèles sont importés
from backend.db.settings import settings


config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# (debug temporaire)
print("ALEMBIC DATABASE URL (str) =", str(settings.DATABASE_URL))
env_pw = os.getenv("DB_PASS", "")
url_pw = getattr(settings.DATABASE_URL, "password", "") or ""
print("ENV pw sha256 first8:", hashlib.sha256(env_pw.encode()).hexdigest()[:8] if env_pw else None)
print("URL pw sha256 first8:", hashlib.sha256(url_pw.encode()).hexdigest()[:8] if url_pw else None)

# Optionnel: injecter dans alembic config (utile en offline)
config.set_main_option("sqlalchemy.url", str(settings.DATABASE_URL))


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = create_engine(
        settings.DATABASE_URL,  # <-- passe l'objet URL directement
        poolclass=NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
