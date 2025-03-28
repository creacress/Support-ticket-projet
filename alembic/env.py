from logging.config import fileConfig
import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# Charger les variables d'env
load_dotenv()

# === CONFIG ALEMBIC ===
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Injecter l'URL de connexion depuis .env
db_url = os.getenv("DATABASE_URL")
if db_url:
    config.set_main_option("sqlalchemy.url", db_url)

# Importer les modèles
from app.database import Base
from app import models

target_metadata = Base.metadata

# === MIGRATIONS ===

def run_migrations_offline():
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
