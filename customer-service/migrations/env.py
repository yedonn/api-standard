from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context
from app.core.config import settings
from app.db.index_model import Base

# Config Alembic
config = context.config

# Configuration des logs
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Définition des métadonnées cibles pour les migrations
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Exécute les migrations en mode 'offline'."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Exécute les migrations en mode 'online'."""
    # Assurez-vous que l'URL est définie correctement
    config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
    connectable = create_engine(settings.DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
